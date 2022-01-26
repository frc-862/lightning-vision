# Usage: Copies files from the directory voidvision on the local device to the directory via scp
# For more information on scp refer to man scp
ssh lightning@10.8.62.10 "rm -rf /lightning-vision/voidvision/*"
scp ../voidvision/* lightning@10.8.62.10:/lightning-vision/voidvision/
