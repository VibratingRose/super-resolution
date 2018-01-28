from __future__ import print_function
import argparse
from torch.utils.data import DataLoader
from SubPixelCNN.solver import SubPixelTrainer
from SRCNN.solver import SRCNNTrainer
from EDSR.solver import EDSRTrainer
from VDSR.solver import VDSRTrainer
from FSRCNN.solver import FSRCNNTrainer
from DRCN.solver import DRCNTrainer
from SRGAN.solver import SRGANTrainer
from dataset.data import get_training_set, get_test_set

# ===========================================================
# Training settings
# ===========================================================
parser = argparse.ArgumentParser(description='PyTorch Super Res Example')
# hyper-parameters
parser.add_argument('--batchSize', type=int, default=8, help='training batch size')
parser.add_argument('--testBatchSize', type=int, default=4, help='testing batch size')
parser.add_argument('--nEpochs', type=int, default=100, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.01, help='Learning Rate. Default=0.01')
parser.add_argument('--seed', type=int, default=123, help='random seed to use. Default=123')

# model configuration
parser.add_argument('--upscale_factor', type=int, default=4, help="super resolution upscale factor")
parser.add_argument('--m', type=str, default='drcn', help='choose which model is going to use')

args = parser.parse_args()


def main():
    # ===========================================================
    # Set train dataset & test dataset
    # ===========================================================
    print('===> Loading datasets')
    train_set = get_training_set(args.upscale_factor)
    test_set = get_test_set(args.upscale_factor)
    training_data_loader = DataLoader(dataset=train_set, batch_size=args.batchSize, shuffle=True)
    testing_data_loader = DataLoader(dataset=test_set, batch_size=args.testBatchSize, shuffle=False)

    if args.m == 'sub':
        model = SubPixelTrainer(args, training_data_loader, testing_data_loader)
    elif args.m == 'srcnn':
        model = SRCNNTrainer(args, training_data_loader, testing_data_loader)
    elif args.m == 'vdsr':
        model = VDSRTrainer(args, training_data_loader, testing_data_loader)
    elif args.m == 'edsr':
        model = EDSRTrainer(args, training_data_loader, testing_data_loader)
    elif args.m == 'fsrcnn':
        model = FSRCNNTrainer(args, training_data_loader, testing_data_loader)
    elif args.m == 'drcn':
        model = DRCNTrainer(args, training_data_loader, testing_data_loader)
    elif args.m == 'srgan':
        model = SRGANTrainer(args, training_data_loader, testing_data_loader)
    else:
        raise Exception("the model does not exist")

    model.validate()


if __name__ == '__main__':
    main()
