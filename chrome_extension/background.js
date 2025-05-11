// 设置每周五早上10点触发一次
chrome.alarms.create('checkUpdates', {
  when: getNextFriday10AM(),
  periodInMinutes: 10080 // 一周的分钟数
});

// 获取下一个周五早上10点的时间戳
function getNextFriday10AM() {
  const now = new Date();
  const nextFriday = new Date();
  
  // 设置时间为早上10点
  nextFriday.setHours(10, 0, 0, 0);
  
  // 计算到下一个周五的天数
  const daysUntilFriday = (5 - now.getDay() + 7) % 7;
  nextFriday.setDate(now.getDate() + daysUntilFriday);
  
  // 如果今天是周五且现在时间已经过了10点，就设置为下周五
  if (daysUntilFriday === 0 && now.getHours() >= 10) {
    nextFriday.setDate(nextFriday.getDate() + 7);
  }
  
  return nextFriday.getTime();
}

// 存储上次更新的内容
let lastContent = '';

// 监听闹钟触发事件
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'checkUpdates') {
    fetchLatestUpdate();
  }
});

// 监听来自popup的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'checkUpdate') {
    fetchLatestUpdate();
    sendResponse({ status: 'started' });
  }
  return true; // 保持消息通道开放
});

// 处理 Markdown 内容
function processMarkdownContent(response) {
  const markdown = response.content;
  const lines = markdown.split('\n');
  let title = 'GitHub 项目更新';
  let content = '';
  let projects = [];
  let updateTime = '';

  for (const line of lines) {
    if (line.startsWith('# ')) {
      title = line.substring(2);
    } else if (line.includes('今日共收集到')) {
      content = line;
    } else if (line.startsWith('## [')) {
      // 提取项目名称
      const match = line.match(/## \[(.*?)\]/);
      if (match) {
        projects.push(match[1]);
      }
    } else if (line.includes('生成时间:')) {
      updateTime = line.split('生成时间:')[1].trim();
    }
  }

  // 构建通知内容
  let notificationContent = content;
  if (projects.length > 0) {
    notificationContent += '\n\n热门项目:\n' + projects.slice(0, 3).join('\n');
  }
  if (updateTime) {
    notificationContent += '\n\n更新时间: ' + updateTime;
  }

  return { 
    title, 
    content: notificationContent,
    viewUrl: response.view_url 
  };
}

// 初始化通知权限
async function initializeNotifications() {
  try {
    // 检查当前权限状态
    const permissionLevel = await new Promise(resolve => {
      chrome.notifications.getPermissionLevel(resolve);
    });
    
    console.log('当前通知权限状态:', permissionLevel);
    
    if (permissionLevel === 'denied') {
      // 尝试请求权限
      const granted = await new Promise(resolve => {
        chrome.permissions.request({
          permissions: ['notifications']
        }, resolve);
      });
      
      console.log('通知权限请求结果:', granted);
      return granted;
    }
    
    return permissionLevel === 'granted';
  } catch (error) {
    console.error('初始化通知权限时出错:', error);
    return false;
  }
}

// 显示通知
async function showNotification(title, message, viewUrl, isUpdate = true) {
  try {
    // 确保有通知权限
    const hasPermission = await initializeNotifications();
    if (!hasPermission) {
      console.error('没有通知权限，无法显示通知');
      return;
    }
    
    // 创建通知
    const notificationOptions = {
      type: 'basic',
      iconUrl: 'icon.png',
      title: isUpdate ? title : 'GitHub 项目检查结果',
      message: isUpdate ? message : '当前无新更新\n' + message,
      priority: 2,
      requireInteraction: true,
      buttons: [{
        title: '查看详情'
      }]
    };
    
    // 存储查看链接，供点击时使用
    chrome.storage.local.set({ 'lastViewUrl': viewUrl });
    
    // 先清除旧的通知
    await new Promise(resolve => {
      chrome.notifications.clear('github-update', resolve);
    });
    
    // 创建新通知
    chrome.notifications.create('github-update', notificationOptions, (notificationId) => {
      if (chrome.runtime.lastError) {
        console.error('创建通知失败:', chrome.runtime.lastError);
        return;
      }
      console.log('通知创建成功，ID:', notificationId);
    });
  } catch (error) {
    console.error('显示通知时出错:', error);
  }
}

// 监听通知点击
chrome.notifications.onClicked.addListener((notificationId) => {
  console.log('通知被点击:', notificationId);
  // 获取并打开查看链接
  chrome.storage.local.get(['lastViewUrl'], result => {
    if (result.lastViewUrl) {
      chrome.tabs.create({ url: result.lastViewUrl });
    }
  });
});

// 监听通知按钮点击
chrome.notifications.onButtonClicked.addListener((notificationId, buttonIndex) => {
  console.log('通知按钮被点击:', notificationId, buttonIndex);
  if (buttonIndex === 0) { // "查看详情" 按钮
    // 获取并打开查看链接
    chrome.storage.local.get(['lastViewUrl'], result => {
      if (result.lastViewUrl) {
        chrome.tabs.create({ url: result.lastViewUrl });
      }
    });
  }
});

// 获取最新更新信息
function fetchLatestUpdate() {
  console.log('正在获取最新更新...');
  fetch('http://127.0.0.1:5000/latest-update')
    .then(response => {
      if (!response.ok) {
        throw new Error('服务器返回错误: ' + response.status);
      }
      return response.json();
    })
    .then(async data => {
      console.log('获取成功，内容长度:', data.content.length);
      
      // 获取上次通知的内容
      const lastNotification = await new Promise(resolve => {
        chrome.storage.local.get(['lastNotification'], result => {
          resolve(result.lastNotification);
        });
      });
      
      const { title, content, viewUrl } = processMarkdownContent(data);
      
      // 检查是否有内容更新
      const hasUpdate = !lastNotification || 
                       lastNotification.title !== title || 
                       lastNotification.message !== content;

      // 无论是否有更新，都显示通知
      showNotification(title, content, viewUrl, hasUpdate);
      
      // 保存本次检查的内容
      chrome.storage.local.set({
        lastNotification: {
          title,
          message: content,
          timestamp: new Date().toISOString(),
          hasUpdate,
          viewUrl
        }
      });
    })
    .catch(error => {
      console.error('获取更新失败:', error);
      showNotification('更新检查失败', error.message, null);
    });
}

// 在扩展安装或更新时初始化
chrome.runtime.onInstalled.addListener(async () => {
  console.log('扩展已安装或更新');
  
  // 初始化通知权限
  const hasPermission = await initializeNotifications();
  console.log('通知权限状态:', hasPermission);
  
  // 设置定时检查为每周五早上10点
  chrome.alarms.create('checkUpdates', {
    when: getNextFriday10AM(),
    periodInMinutes: 10080
  });
  
  // 立即检查更新
  fetchLatestUpdate();
});