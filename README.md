# 打砖块游戏项目文档

## 📜 项目概览
- **名称**：打砖块（Arkanoid）
- **类型**：2D 街机类游戏
- **框架**：Pygame Zero (Python 3.7+)
- **目标平台**：Windows

## 🎮 核心功能
### 基础玩法
- **弹球物理**  
  支持速度调整、挡板反弹角度计算
- **砖块破坏**  
  多种耐久度砖块（命中1次/3次可击碎）
  ```python
  bricks = [
      {"pos": (x, y), "color": color, "durability": 3}
  ]
