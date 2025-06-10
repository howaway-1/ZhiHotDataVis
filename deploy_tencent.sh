#!/bin/bash

# 腾讯云部署脚本
# 使用前请确保已安装腾讯云CLI工具

echo "=== 知乎热榜数据可视化系统 - 腾讯云部署脚本 ==="

# 配置变量
PROJECT_NAME="zhihu-hot-vis"
REGION="ap-beijing"  # 可选: ap-shanghai, ap-guangzhou
INSTANCE_TYPE="S5.MEDIUM2"  # 2核4GB
IMAGE_ID="img-eb30mz89"  # Ubuntu 20.04

# 检查腾讯云CLI是否已安装
if ! command -v tccli &> /dev/null; then
    echo "错误: 腾讯云CLI未安装，请先安装tccli"
    echo "安装命令: pip install tccli"
    exit 1
fi

# 检查是否已配置腾讯云凭证
if ! tccli configure list &> /dev/null; then
    echo "错误: 腾讯云凭证未配置，请先配置"
    echo "配置命令: tccli configure"
    exit 1
fi

echo "1. 创建安全组..."
SECURITY_GROUP_ID=$(tccli cvm CreateSecurityGroup \
    --region $REGION \
    --GroupName "${PROJECT_NAME}-sg" \
    --GroupDescription "知乎热榜系统安全组" \
    --query 'SecurityGroup.SecurityGroupId' \
    --output text)

echo "安全组ID: $SECURITY_GROUP_ID"

echo "2. 配置安全组规则..."
# 允许SSH (22端口)
tccli cvm AuthorizeSecurityGroupPolicies \
    --region $REGION \
    --SecurityGroupId $SECURITY_GROUP_ID \
    --SecurityGroupPolicySet '{
        "Ingress": [
            {
                "Protocol": "TCP",
                "Port": "22",
                "CidrBlock": "0.0.0.0/0",
                "Action": "ACCEPT",
                "PolicyDescription": "SSH访问"
            },
            {
                "Protocol": "TCP",
                "Port": "80",
                "CidrBlock": "0.0.0.0/0",
                "Action": "ACCEPT",
                "PolicyDescription": "HTTP访问"
            },
            {
                "Protocol": "TCP",
                "Port": "443",
                "CidrBlock": "0.0.0.0/0",
                "Action": "ACCEPT",
                "PolicyDescription": "HTTPS访问"
            },
            {
                "Protocol": "TCP",
                "Port": "5000",
                "CidrBlock": "0.0.0.0/0",
                "Action": "ACCEPT",
                "PolicyDescription": "Flask应用"
            }
        ]
    }'

echo "3. 创建云服务器实例..."
INSTANCE_ID=$(tccli cvm RunInstances \
    --region $REGION \
    --InstanceChargeType POSTPAID_BY_HOUR \
    --InstanceType $INSTANCE_TYPE \
    --ImageId $IMAGE_ID \
    --SystemDisk '{
        "DiskType": "CLOUD_PREMIUM",
        "DiskSize": 50
    }' \
    --InternetAccessible '{
        "InternetChargeType": "TRAFFIC_POSTPAID_BY_HOUR",
        "InternetMaxBandwidthOut": 10,
        "PublicIpAssigned": true
    }' \
    --InstanceCount 1 \
    --InstanceName "${PROJECT_NAME}-server" \
    --SecurityGroupIds "[$SECURITY_GROUP_ID]" \
    --query 'InstanceIdSet[0]' \
    --output text)

echo "实例ID: $INSTANCE_ID"

echo "4. 等待实例启动..."
sleep 30

# 获取公网IP
PUBLIC_IP=$(tccli cvm DescribeInstances \
    --region $REGION \
    --InstanceIds "[$INSTANCE_ID]" \
    --query 'InstanceSet[0].PublicIpAddresses[0]' \
    --output text)

echo "公网IP: $PUBLIC_IP"

echo "5. 生成部署脚本..."
cat > remote_deploy.sh << 'EOF'
#!/bin/bash

echo "=== 服务器端部署脚本 ==="

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装Git
sudo apt install -y git

# 克隆项目（需要替换为您的Git仓库地址）
# git clone https://github.com/yourusername/zhihu-hot-vis.git
# cd zhihu-hot-vis

echo "请手动上传项目文件到服务器，然后运行以下命令："
echo "cd /path/to/your/project"
echo "docker-compose up -d"

EOF

echo "=== 部署完成 ==="
echo "服务器信息:"
echo "  实例ID: $INSTANCE_ID"
echo "  公网IP: $PUBLIC_IP"
echo "  安全组ID: $SECURITY_GROUP_ID"
echo ""
echo "下一步操作:"
echo "1. 使用SSH连接到服务器: ssh ubuntu@$PUBLIC_IP"
echo "2. 上传项目文件到服务器"
echo "3. 运行部署脚本: bash remote_deploy.sh"
echo "4. 启动应用: docker-compose up -d"
echo ""
echo "访问地址: http://$PUBLIC_IP:5000"
