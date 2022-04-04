from re import X
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os



class Linear_QNet(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)

        return X

    def save(self, file_name='model.pth'):
        model_folder = './model'
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)
        
        file_name = os.path.join(model_folder, file_name)

        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma
        self.model = model

        self.optimizer = optim.Adam(model.parameters(), lr=self.alpha)
        self.critirion = nn.MSELoss()

    
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)

            done = (done, )
        
        #predicted Q value

        prediction = self.model(state)

        target = prediction.clone()

        for index in range(len(done)):
            Q_new = reward[index]
            if not done[index]:
                Q_new = reward[index] + self.gamma * torch.max(self.model(next_state[index]))


            target[index][torch.argmax(action).item()] = Q_new
        
        #new Q = r + gamma * max(next_predicted Q)

        self.optimizer.zero_grad()

        loss = self.critirion(target, prediction)
        loss.backward()



        self.optimizer.step()



