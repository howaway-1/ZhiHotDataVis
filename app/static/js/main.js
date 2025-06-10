// 页面加载完成后执行侧边栏和警告框功能
document.addEventListener('DOMContentLoaded', function() {
    // 侧边栏折叠功能
    initSidebar();
    
    // 警告框自动关闭
    initAlerts();
});

// 初始化侧边栏功能
function initSidebar() {
    console.log("初始化侧边栏功能...");
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (!sidebarToggle || !sidebar || !mainContent) {
        console.error("未找到侧边栏相关元素");
        return;
    }
    
    // 检查本地存储中的侧边栏状态
    const sidebarState = localStorage.getItem('sidebarCollapsed');
    
    // 如果之前已收起，则应用收起状态
    if (sidebarState === 'true') {
        sidebar.classList.add('sidebar-collapsed');
        mainContent.style.marginLeft = '70px'; // 使用固定值确保正确应用
    } else {
        sidebar.classList.remove('sidebar-collapsed');
        mainContent.style.marginLeft = '240px'; // 使用固定值确保正确应用
    }
    
    // 侧边栏切换按钮点击事件
    sidebarToggle.addEventListener('click', function() {
        console.log("侧边栏切换按钮被点击");
        sidebar.classList.toggle('sidebar-collapsed');
        
        // 根据侧边栏状态调整主内容区域
        if (sidebar.classList.contains('sidebar-collapsed')) {
            mainContent.style.marginLeft = '70px';
            localStorage.setItem('sidebarCollapsed', 'true');
        } else {
            mainContent.style.marginLeft = '240px';
            localStorage.setItem('sidebarCollapsed', 'false');
        }
    });
    
    // 响应式移动设备处理
    if (window.innerWidth < 992) {
        mainContent.style.marginLeft = '0';
        
        document.addEventListener('click', function(event) {
            // 如果点击的不是侧边栏内部元素且不是切换按钮
            if (!sidebar.contains(event.target) && event.target !== sidebarToggle) {
                sidebar.classList.remove('show');
            }
        });
        
        sidebarToggle.addEventListener('click', function(event) {
            event.stopPropagation();
            sidebar.classList.toggle('show');
        });
    }
}

// 初始化警告框自动关闭功能
function initAlerts() {
    // 确保存在警告框容器
    let alertContainer = document.querySelector('.custom-alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'custom-alert-container';
        document.body.appendChild(alertContainer);
    }
    
    // 处理已存在的警告框
    const alerts = document.querySelectorAll('.alert-dismissible, .custom-alert');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // 淡出效果
            alert.style.opacity = '0';
            alert.classList.add('hide');
            
            // 移除元素
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000); // 5秒后自动关闭
    });
}

/**
 * 显示自定义警告框
 * @param {string} message - 警告消息
 * @param {string} type - 警告类型 (success, danger, warning, info)
 * @param {boolean} dismissible - 是否可关闭
 * @param {number} duration - 自动关闭时间(毫秒)，0表示不自动关闭
 */
function showAlert(message, type = 'info', dismissible = true, duration = 5000) {
    // 确保存在警告框容器
    let alertContainer = document.querySelector('.custom-alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'custom-alert-container';
        document.body.appendChild(alertContainer);
    }
    
    // 创建警告框
    const alert = document.createElement('div');
    alert.className = `custom-alert alert-${type}`;
    
    // 设置内容
    let alertContent = `
        <div class="alert-icon">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 
                              type === 'danger' ? 'times-circle' : 
                              type === 'warning' ? 'exclamation-triangle' : 
                              'info-circle'}"></i>
        </div>
        <div class="alert-content">${message}</div>
    `;
    
    if (dismissible) {
        alertContent += `
            <button type="button" class="close" aria-label="关闭">
                <span aria-hidden="true">&times;</span>
            </button>
        `;
    }
    
    alert.innerHTML = alertContent;
    
    // 添加到容器
    alertContainer.prepend(alert);
    
    // 添加关闭按钮事件
    if (dismissible) {
        const closeBtn = alert.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.opacity = '0';
                alert.classList.add('hide');
                
                setTimeout(function() {
                    alert.remove();
                }, 300);
            });
        }
    }
    
    // 如果设置了持续时间，自动关闭
    if (duration > 0) {
        setTimeout(function() {
            // 淡出效果
            alert.style.opacity = '0';
            alert.classList.add('hide');
            
            // 移除元素
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, duration);
    }
    
    return alert;
}

// 初始化ECharts图表并应用modern主题
function initEchart(elementId) {
    // 检查元素是否存在
    if (!document.getElementById(elementId)) return null;
    
    // 使用modern主题初始化图表
    const chart = echarts.init(document.getElementById(elementId), 'modern');
    
    // 添加窗口大小调整时自动调整图表大小
    window.addEventListener('resize', function() {
        chart.resize();
    });
    
    return chart;
}

// DOM就绪时执行
$(document).ready(function() {
    // ... existing code ...
}); 