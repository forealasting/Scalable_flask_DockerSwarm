import torch


print(torch.cuda.is_available())


print(torch.cuda.device_count())


print(torch.cuda.current_device())


a = [1, 2, 3]
a = [x+1 for x in a]

f = 1
while True:
    if f == 1:
        break
    print('not finish ')


b = [i for i in range(100)]
print(b[-10:])

