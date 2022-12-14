import pandas as pd
import torch
import MyFunction
import read_dataset
from torch.utils.data import DataLoader
import MyNet
import csv
import numpy as np
import time

start_time = time.time()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# input data
input_data = pd.read_csv('targets/target1.csv')
target = input_data['OCCUPANCY'].values.astype('float64')
target = torch.as_tensor(target, device=device).float()

#Past Impl: Debug variables
testing = False
delete = True
mod = 10

#These are valuable to change iterations and epoch number
epoch_num = 100
times = 2

output_matrix = torch.zeros([epoch_num, times*6])
errors = 0

test_size = len(target) - int(len(target)*0.8) - 6*2
occ_list = np.zeros([test_size, times])


#Past Impl: Reminder to start Past if we are testing
if(testing is True):
    input("Press enter after starting Past, if unsure how to do so read the research_README.txt file in the ALL-main directory:")

for t in range(times):
    if delete is True and t != 0 and t%1 == 0:
        output_matrix = torch.zeros([epoch_num, (times)*6])
        errors += 1
    # init network
    net = MyNet.MyLSTMNet(input_size=1, hidden_size=1, seq_len=6, output_size=1, num_layers=1).to(device)  # Choose baseline net
    loss_function = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.02)

    # input data
    support_size = int(len(target) * 0.6)
    query_size = int(len(target) * 0.8)
    support_target = target[support_size:query_size]
    query_target = target[query_size:]
    support_set = read_dataset.MyData(support_target, seq_length=6)
    query_set = read_dataset.MyData(query_target, seq_length=6)
    support_loader = DataLoader(support_set, batch_size=len(support_set), shuffle=False)
    query_loader = DataLoader(query_set, batch_size=len(query_set), shuffle=False)

    fine_tuning_loss_list = torch.zeros([epoch_num])
    test_loss_list = torch.zeros([epoch_num])
    RMSE_list = torch.zeros([epoch_num])
    MAPE_list = torch.zeros([epoch_num])
    R2_list = torch.zeros([epoch_num])
    RAE_list = torch.zeros([epoch_num])

    for epoch in range(epoch_num):
        if (epoch+1) % 10 == 0:
            print("epoch_num =", epoch+1, "/", epoch_num)
        # fine-tuning
        for i, support in enumerate(support_loader):
            support_sample, support_label = support
            optimizer.zero_grad()
            output = net(support_sample)
            output = torch.squeeze(output)
            loss = loss_function(output, support_label)
            loss.backward()
            optimizer.step()
            fine_tuning_loss_list[epoch] = loss.item()
        # testing
        count = 0;
        for i, query in enumerate(query_loader):
            query_sample, query_label = query
            optimizer.zero_grad()
            output = net(query_sample)
            output = torch.squeeze(output)
            loss = loss_function(output, query_label)
            test_loss_list[epoch] = loss.item()

            # output metrics
            output = torch.reshape(output, [len(query_label)]).cpu()
            output = output.detach().numpy()
            query_label = torch.reshape(query_label, [len(query_label)]).cpu()
            query_label = query_label.detach().numpy()

            # calculate MAPE
            MAPE = np.mean(abs(output - query_label) / query_label) * 100
            # RMSE
            RMSE = np.sqrt(np.mean((output - query_label)*(output - query_label))) * 100
            # R2
            SSE = np.sum((output - query_label)*(output - query_label))
            SST =np.sum((np.mean(query_label) - query_label)*(np.mean(query_label) - query_label))
            R2_score = (1 - SSE / SST) * 100
            # RAE
            RAE = np.sum(abs(output - query_label)) / np.sum(abs(np.mean(query_label) - query_label)) * 100

            RMSE_list[epoch] = RMSE
            MAPE_list[epoch] = MAPE
            R2_list[epoch] = R2_score
            RAE_list[epoch] = RAE
            count+=1

        output_matrix[:, 6 * t + 0] = RMSE_list #Root Mean Square Error
        output_matrix[:, 6 * t + 1] = MAPE_list #Mean absolute percentage error
        output_matrix[:, 6 * t + 2] = R2_list #Coefficient of Determination
        output_matrix[:, 6 * t + 3] = RAE_list
        output_matrix[:, 6 * t + 4] = fine_tuning_loss_list
        output_matrix[:, 6 * t + 5] = test_loss_list
    #Past Impl: Saves matrix to a file to send to Past
    if(t%mod == 0 and testing is True):
        torch.save(output_matrix, "outputmatrix.pt")
        input("Press enter after using Past to send output matrix:")

    # Past Impl: Read matrix from pl file to output_matrix (restores deleted matrix)
    if(t == 1 and testing is True):
        output_matrix = 0   #feints deletion of matrix
        input("Press enter after using Past to retrieve input matrix:")
        # output_matrix = np.genfromtxt('inputmatrix.txt',delimiter=' ')
        output_matrix = torch.load('inputmatrix.pt')

    occ_list[:, t] = output

# print final metrics
print('RMSE =', RMSE)
print('MAPE =', MAPE)
print('R2 =', R2_score)
print('RAE =', RAE)
print('Errors =', errors)


#Past Impl: saves one final outputmatrix pl file
torch.save(output_matrix,"outputmatrix.pt")

# output loss
output = output_matrix
f = open('result/Baseline_target1_metrics.csv', 'w', newline='')
csv_writer = csv.writer(f)
for l in output:
    csv_writer.writerow(l)
f.close()

# output loss
output = occ_list
f = open('result/Baseline_target1_occupancy.csv', 'w', newline='')
csv_writer = csv.writer(f)
for l in output:
    csv_writer.writerow(l)
f.close()

print("--- %s seconds ---" % (time.time() - start_time))


