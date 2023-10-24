import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class HGNN_AC(nn.Module):
    def __init__(self, in_dim, hidden_dim, dropout, activation, num_heads, cuda=False):
        super(HGNN_AC, self).__init__()
        self.dropout = dropout
        self.attentions = [AttentionLayer(in_dim, hidden_dim, dropout, activation, cuda) for _ in range(num_heads)]

        for i, attention in enumerate(self.attentions):
            self.add_module('attention_{}'.format(i), attention)
        self.fc = nn.Linear(num_heads, 1)
    def forward(self, bias, emb_dest, emb_src, feature_src):
        adj = F.dropout(bias, self.dropout, training=self.training)
        x = torch.cat([att(adj, emb_dest, emb_src, feature_src).unsqueeze(0) for att in self.attentions], dim=0)

        # ## no att
        # output_tensor = torch.mm(torch.mm(emb_dest, emb_src.t()), feature_src)

        # mean
        output_tensor = torch.mean(x, dim=0, keepdim=False)

        ## linear
        # x_shapes = x.shape
        # input_tensor = x.view(-1, x_shapes[0])
        # # 将重塑后的输入张量传递给nn.Linear层进行线性变换
        # output_tensor = self.fc(input_tensor)
        # # 将输出张量重塑为三维张量
        # output_tensor = output_tensor.view(x.shape[1], x.shape[2])
        return output_tensor


class AttentionLayer(nn.Module):
    def __init__(self, in_dim, hidden_dim, dropout, activation, cuda=False):
        super(AttentionLayer, self).__init__()
        self.dropout = dropout
        self.activation = activation
        self.is_cuda = cuda

        self.W = nn.Parameter(nn.init.xavier_normal_(
            torch.Tensor(in_dim, hidden_dim).type(torch.cuda.FloatTensor if cuda else torch.FloatTensor),
            gain=np.sqrt(2.0)), requires_grad=True)
        self.W2 = nn.Parameter(nn.init.xavier_normal_(torch.Tensor(hidden_dim, hidden_dim).type(
            torch.cuda.FloatTensor if cuda else torch.FloatTensor), gain=np.sqrt(2.0)),
            requires_grad=True)

        self.leakyrelu = nn.LeakyReLU(0.2)

    def forward(self, bias, emb_dest, emb_src, feature_src):
        h_1 = torch.mm(emb_src, self.W)
        h_2 = torch.mm(emb_dest, self.W)

        e = self.leakyrelu(torch.mm(torch.mm(h_2, self.W2), h_1.t()))
        zero_vec = -9e15 * torch.ones_like(e)

        attention = torch.where(bias > 0, e, zero_vec)
        attention = F.softmax(attention, dim=1)
        attention = F.dropout(attention, self.dropout, training=self.training)
        h_prime = torch.matmul(attention, feature_src)

        return self.activation(h_prime)
