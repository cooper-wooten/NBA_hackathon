clear all
close all
clc

%% Read Data
training_data = csvread('new_train.csv',1,5);
training_data = repmat(training_data,5,1);
input = training_data(:,1:end-1);
target = training_data(:,end);

%% Neural Net
%{
net = feedforwardnet([10 10 10 10 10]);

net.trainFcn = 'trainscg';
net.trainParam.epochs = 5000;
net.trainParam.max_fail = 500;

net = configure(net,input,target);

[net,tr] = train(net,input,target);
output = net(input);

o = target(1:2000);
new_output = [];
new_target = [];
for i = 1:length(o)
    if o(i) > 10000
        new_output = [new_output output(i)];
        new_target = [new_target o(i)];
    end
end


plot(target(451:480),'o')
hold on
plot(output(451:480),'o')
hold off
legend('target','output')
%}
%% Regression Tree

Model = TreeBagger(100, input, target, 'Method', 'Regression');
    

tree = fitrtree(input,target);
leafs = linspace(1,100,10);
branches = linspace(10,1000,10);

rng 'default';
N = numel(leafs);
NN = numel(branches);

err = zeros(N,NN);
for n=1:N
    for nn=1:NN
        tree = fitrtree(input,target,'CrossVal','On',...
            'MinLeafSize',leafs(n),'MinParentSize',branches(nn),'KFold',5);
        err(n,nn) = kfoldLoss(tree);
    end
end

