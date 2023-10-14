import torch
import matplotlib.pyplot as plt
from torchvision import transforms

from dataset import SuperResolutionDataset
from modules import ESPCN
import numpy as np

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load the model
model = ESPCN().to(DEVICE)
model.load_state_dict(torch.load('best_model.pth'))
model.eval()

# Create test dataset
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
test_dataset = SuperResolutionDataset(root_dir='AD_NC', transform=None, mode='test')

# Process a few images from the test set
num_images_to_show = 3
fig, axes = plt.subplots(num_images_to_show, 3, figsize=(15, 15))

# Titles for plots
titles = ['Low Resolution', 'Predicted High Resolution', 'Original High Resolution']

for ax, title in zip(axes[0], titles):
    ax.set_title(title)


def denormalize(tensor):
    return tensor * 0.5 + 0.5


for idx in range(num_images_to_show):
    lr_tensor, hr_tensor = test_dataset[idx]

    # Move tensors to device
    lr_tensor = lr_tensor.unsqueeze(0).to(DEVICE)

    # Predict using the model
    with torch.no_grad():
        pred_hr_tensor = model(lr_tensor)

    # Convert tensors back to images
    lr_image = transforms.ToPILImage()(denormalize(lr_tensor.squeeze().cpu()))
    pred_hr_image = transforms.ToPILImage()(denormalize(pred_hr_tensor.squeeze().cpu().detach()))
    hr_image = transforms.ToPILImage()(denormalize(hr_tensor.cpu()))
    print(pred_hr_image)

    # Display images
    axes[idx, 0].imshow(np.asarray(lr_image), cmap='gray')
    axes[idx, 1].imshow(np.asarray(pred_hr_image), cmap='gray')
    axes[idx, 2].imshow(np.asarray(hr_image), cmap='gray')

    # Remove axis ticks
    for ax in axes[idx]:
        ax.set_xticks([])
        ax.set_yticks([])

plt.tight_layout()
plt.show()
