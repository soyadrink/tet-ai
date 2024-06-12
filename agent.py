import torch
import random
import numpy as np
from collections import deque
from tetris_ai import Tetris
from model import Linear_QNet, QTrainer
from plotter import plot
import os

MAX_MEMORY = 100000
BATCH_SIZE = 400
LR = 0.001

class Agent:
    def __init__(self):
        self.num_of_games = 0
        self.record = 0
        self.total = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(215, 1024, 8).to(device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
        self.load_state()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def load_state(self, file_name="model.pth"):
        # also load plot data maybe
        model_folder_path = "./model"
        model_path = os.path.join(model_folder_path, file_name)
        if not os.path.exists(model_path):
            print("Model path does not exist")
        else:
            file_name = os.path.join(model_folder_path, file_name)
            self.data = torch.load(file_name)
            self.model.load_state_dict(self.data["model"])
            self.model.eval()
            self.num_of_games = self.data["games"]
            self.record = self.data["record"]
            self.total = self.data["total"]

    def get_state(self, game):
        board = [i for j in game.game.grid.grid for i in j]
        position_rotation = [i for j in [[k.row, k.col] for k in game.game.current_tetromino.get_cell_positions()] for i in j]
        next_tetrominos = [game.game.next_tetromino1.id, game.game.next_tetromino2.id, game.game.next_tetromino3.id, game.game.next_tetromino4.id, game.game.next_tetromino5.id]
        held_tetromino = [game.game.held_tetromino.id]
        holdable = [0 if game.game.pre_held == True else 1]
        state = board + position_rotation + next_tetrominos + held_tetromino + holdable
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def get_action(self, state):
        self.epsilon = 600 - self.num_of_games
        final_move = [0, 0, 0, 0, 0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 7)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            state0 = state0.to(device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train():
    agent = Agent()
    game = Tetris()
    plot_scores = []
    plot_average_scores = []
    record = agent.record
    total_score = agent.total
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        agent.remember(state_old, final_move, reward, state_new, game_over)
        agent.get_state(game)
        if game_over:
            game.reset()
            agent.num_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save("model.pth", agent.num_of_games, record, total_score)
            
            print(f"Game: {agent.num_of_games} | Reward: {reward} | Score: {score} | Record: {record}")
            plot_scores.append(score)
            total_score += score
            average_score = total_score / agent.num_of_games
            plot_average_scores.append(average_score)
            plot(plot_scores, plot_average_scores)

if __name__ == "__main__":
    train()