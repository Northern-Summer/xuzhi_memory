# WSL 只读挂载配置指南

## 目标

- Windows C:\ D:\ 默认只读
- 只保留 `/mnt/c/Users/MzgyM/wechat_rpa/` 可写

---

## 方案 1：修改 /etc/wsl.conf（推荐）

在 WSL 中创建/编辑 `/etc/wsl.conf`：

```bash
sudo nano /etc/wsl.conf
```

添加以下内容：

```ini
[boot]
systemd=true

[automount]
enabled=true
options="ro,metadata"
mountFsTab=true
```

然后创建 `/etc/fstab` 覆盖特定目录：

```bash
sudo nano /etc/fstab
```

添加：

```
# 共享目录可写
C:\Users\MzgyM\wechat_rpa /mnt/c/Users/MzgyM/wechat_rpa drvfs rw,noatime,uid=1000,gid=1000 0 0
```

最后重启 WSL：

```powershell
# 在 Windows PowerShell 中
wsl --shutdown
```

---

## 方案 2：使用 .wslconfig（Windows 端配置）

编辑 `C:\Users\MzgyM\.wslconfig`：

```ini
[wsl2]
memory=4GB
processors=8
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
firewall=true
localhostForwarding=true
guiApplications=true

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
hostAddressLoopback=true

# 新增：默认只读挂载
[automount]
options="ro,metadata"
```

重启 WSL：

```powershell
wsl --shutdown
```

---

## 方案 3：手动重新挂载（临时）

在 WSL 中执行：

```bash
# 将 C: 重新挂载为只读
sudo mount -o remount,ro /mnt/c

# 将 D: 重新挂载为只读
sudo mount -o remount,ro /mnt/d

# 将共享目录重新挂载为可写
sudo mount -o remount,rw /mnt/c/Users/MzgyM/wechat_rpa
```

注意：这个方案在 WSL 重启后会失效。

---

## 验证

```bash
# 测试只读
touch /mnt/c/test.txt
# 应该报错: Read-only file system

# 测试共享目录可写
touch /mnt/c/Users/MzgyM/wechat_rpa/queue/test.txt
echo "test" > /mnt/c/Users/MzgyM/wechat_rpa/queue/test.txt
cat /mnt/c/Users/MzgyM/wechat_rpa/queue/test.txt
rm /mnt/c/Users/MzgyM/wechat_rpa/queue/test.txt
# 应该成功
```

---

## 推荐方案

**方案 1** 最为可靠，修改后永久生效。

执行步骤：

```bash
# 1. 备份当前配置
sudo cp /etc/wsl.conf /etc/wsl.conf.bak

# 2. 编辑配置
sudo nano /etc/wsl.conf

# 3. 在 Windows 中重启 WSL
# wsl --shutdown

# 4. 重新进入 WSL 验证
```

---

*Created: 2026-04-01*
