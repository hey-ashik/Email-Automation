/**
 * Email Automation Dashboard - Frontend Logic
 * Handles all UI interactions and API calls
 */

// Global variables
let currentFile = null;
let statusCheckInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeFileUpload();
    initializeConfigForm();
    loadConfiguration();
    startStatusPolling();
});

/**
 * Sidebar Navigation
 */
function initializeSidebar() {
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const navItems = document.querySelectorAll('.nav-item');

    // Toggle sidebar on mobile
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.add('active');
            overlay.classList.add('active');
        });
    }

    // Close sidebar
    if (closeSidebar) {
        closeSidebar.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    }

    // Navigate between sections
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.dataset.section;
            
            // Update active nav item
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            // Show corresponding section
            document.querySelectorAll('.content-section').forEach(sec => {
                sec.classList.remove('active');
            });
            document.getElementById(`${section}-section`).classList.add('active');
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
                overlay.classList.remove('active');
            }
        });
    });
}

/**
 * File Upload Handling
 */
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = 'var(--light-gray)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '';
        uploadArea.style.background = '';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '';
        uploadArea.style.background = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

/**
 * Handle file upload
 */
function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    showToast('Uploading file...', 'info');

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentFile = data.filepath;
            document.getElementById('fileName').textContent = data.filename;
            displayDataPreview(data.preview);
            document.getElementById('filePreview').style.display = 'block';
            document.getElementById('uploadArea').style.display = 'none';
            
            // Update send section with actual total from file
            document.getElementById('dataSourceInfo').textContent = data.filename;
            document.getElementById('totalEmails').textContent = data.total_emails || data.preview.length;
            
            showToast('File uploaded successfully!', 'success');
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Error uploading file: ' + error.message, 'error');
    });
}

/**
 * Clear uploaded file
 */
function clearFile() {
    currentFile = null;
    document.getElementById('filePreview').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('fileInput').value = '';
    document.getElementById('dataSourceInfo').textContent = 'No file loaded';
    document.getElementById('totalEmails').textContent = '0';
}

/**
 * Display data preview
 */
function displayDataPreview(data) {
    const previewDiv = document.getElementById('dataPreview');
    
    if (!data || data.length === 0) {
        previewDiv.innerHTML = '<p>No data to preview</p>';
        return;
    }

    let table = '<table><thead><tr>';
    
    // Headers
    const headers = Object.keys(data[0]);
    headers.forEach(header => {
        table += `<th>${header}</th>`;
    });
    table += '</tr></thead><tbody>';
    
    // Rows
    data.forEach(row => {
        table += '<tr>';
        headers.forEach(header => {
            table += `<td>${row[header] || ''}</td>`;
        });
        table += '</tr>';
    });
    
    table += '</tbody></table>';
    previewDiv.innerHTML = table;
}

/**
 * Load Google Sheet
 */
function loadGoogleSheet() {
    const url = document.getElementById('googleSheetUrl').value;
    
    if (!url) {
        showToast('Please enter a Google Sheets URL', 'warning');
        return;
    }

    showToast('Loading Google Sheet...', 'info');

    fetch('/api/google-sheet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentFile = data.filepath;
            displayDataPreview(data.preview);
            document.getElementById('sheetPreview').style.display = 'block';
            
            // Update send section with actual total from file
            document.getElementById('dataSourceInfo').textContent = 'Google Sheet';
            document.getElementById('totalEmails').textContent = data.total_emails || data.preview.length;
            
            showToast('Google Sheet loaded successfully!', 'success');
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Error loading Google Sheet: ' + error.message, 'error');
    });
}

/**
 * Configuration Form
 */
function initializeConfigForm() {
    const configForm = document.getElementById('configForm');
    
    configForm.addEventListener('submit', (e) => {
        e.preventDefault();
        saveConfiguration();
    });
}

/**
 * Load configuration
 */
function loadConfiguration() {
    fetch('/api/config')
    .then(response => response.json())
    .then(config => {
        document.getElementById('senderName').value = config.sender_name || '';
        document.getElementById('senderEmail').value = config.sender_email || '';
        document.getElementById('smtpServer').value = config.smtp_server || 'smtp.gmail.com';
        document.getElementById('smtpPort').value = config.smtp_port || 587;
        
        // Don't load password for security
        if (config.has_password) {
            document.getElementById('senderPassword').placeholder = '••••••••••••••••';
        }
    })
    .catch(error => {
        console.error('Error loading config:', error);
    });
}

/**
 * Save configuration
 */
function saveConfiguration() {
    const config = {
        sender_name: document.getElementById('senderName').value,
        sender_email: document.getElementById('senderEmail').value,
        sender_password: document.getElementById('senderPassword').value,
        smtp_server: document.getElementById('smtpServer').value,
        smtp_port: parseInt(document.getElementById('smtpPort').value)
    };

    showToast('Saving configuration...', 'info');

    fetch('/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Configuration saved successfully!', 'success');
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Error saving configuration: ' + error.message, 'error');
    });
}

/**
 * Test email connection
 */
function testConnection() {
    showToast('Connection test feature coming soon!', 'info');
}

/**
 * Start sending emails
 */
function startSending() {
    if (!currentFile) {
        showToast('Please upload a file first!', 'warning');
        return;
    }

    const senderName = document.getElementById('senderName').value;

    showToast('Starting email sending...', 'info');

    fetch('/api/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            filepath: currentFile,
            sender_name: senderName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('startSendBtn').style.display = 'none';
            document.getElementById('stopSendBtn').style.display = 'inline-flex';
            document.getElementById('sendProgress').style.display = 'block';
            
            updateStatusIndicator('sending');
            showToast('Email sending started!', 'success');
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Error starting email send: ' + error.message, 'error');
    });
}

/**
 * Stop sending emails
 */
function stopSending() {
    fetch('/api/stop', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('startSendBtn').style.display = 'inline-flex';
            document.getElementById('stopSendBtn').style.display = 'none';
            document.getElementById('sendProgress').style.display = 'none';
            
            updateStatusIndicator('ready');
            showToast('Email sending stopped', 'warning');
        }
    })
    .catch(error => {
        showToast('Error stopping emails: ' + error.message, 'error');
    });
}

/**
 * Start polling for status updates
 */
function startStatusPolling() {
    statusCheckInterval = setInterval(checkStatus, 2000); // Check every 2 seconds
}

/**
 * Check sending status
 */
function checkStatus() {
    fetch('/api/status')
    .then(response => response.json())
    .then(data => {
        // Update total emails if we have it
        if (data.total_emails > 0) {
            document.getElementById('totalEmails').textContent = data.total_emails;
        }
        
        // Update sent and failed counts from backend
        if (data.sent_count !== undefined) {
            document.getElementById('sentCount').textContent = data.sent_count;
        }
        if (data.failed_count !== undefined) {
            document.getElementById('failedCount').textContent = data.failed_count;
        }
        
        if (data.is_sending) {
            updateStatusIndicator('sending');
            updateSendingProgress(data);
            document.getElementById('sendProgress').style.display = 'block';
            
            // Mark that we're in an active sending session
            window.wasJustSending = true;
        } else {
            updateStatusIndicator('ready');
            document.getElementById('startSendBtn').style.display = 'inline-flex';
            document.getElementById('stopSendBtn').style.display = 'none';
            
            // Check if sending just completed (transition from sending to not sending)
            const totalEmails = data.total_emails || parseInt(document.getElementById('totalEmails').textContent) || 0;
            const processed = data.sent_count + data.failed_count;
            
            // Show completion notification ONLY when we just finished sending (wasJustSending === true)
            // and we have completed all emails
            if (window.wasJustSending && totalEmails > 0 && processed === totalEmails && processed > 0) {
                window.wasJustSending = false; // Reset flag immediately
                showCompletionNotification(data.sent_count, data.failed_count, totalEmails);
            }
            
            // Hide progress when not sending and no emails processed
            if (data.sent_count === 0 && data.failed_count === 0) {
                document.getElementById('sendProgress').style.display = 'none';
                window.wasJustSending = false; // Reset flag when counters are cleared
            }
        }
        
        // Don't update logs from status check - rely on backend counts
    })
    .catch(error => {
        console.error('Status check error:', error);
    });
}

/**
 * Update sending progress
 */
function updateSendingProgress(data) {
    // Use backend counts for accurate progress
    const totalEmails = data.total_emails || parseInt(document.getElementById('totalEmails').textContent) || 0;
    const processed = data.sent_count + data.failed_count;
    
    if (totalEmails > 0) {
        const progress = (processed / totalEmails) * 100;
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('progressText').textContent = 
            `Sending... ${processed} of ${totalEmails}`;
    }
}

/**
 * Update log counts
 */
function updateLogCounts(logs) {
    let sent = 0, failed = 0;
    
    logs.forEach(log => {
        if (log.status === 'Sent') sent++;
        else if (log.status === 'Failed') failed++;
    });
    
    document.getElementById('sentCount').textContent = sent;
    document.getElementById('failedCount').textContent = failed;
}

/**
 * Load and display all logs
 */
function loadLogs() {
    fetch('/api/logs')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayLogs(data.logs);
        }
    })
    .catch(error => {
        console.error('Error loading logs:', error);
    });
}

/**
 * Display logs
 */
function displayLogs(logs) {
    const logsContainer = document.getElementById('logsContainer');
    
    if (!logs || logs.length === 0) {
        logsContainer.innerHTML = '<p class="empty-state">No logs yet. Start sending emails to see activity here.</p>';
        return;
    }

    let html = '';
    logs.reverse().forEach(log => {
        const statusClass = log.status.toLowerCase();
        html += `
            <div class="log-entry ${statusClass}">
                <div class="log-header">
                    <span class="log-to">${log.to}</span>
                    <span class="log-time">${log.timestamp}</span>
                </div>
                <div class="log-subject">${log.subject}</div>
                <div class="log-status ${statusClass}">
                    ${log.status}: ${log.message}
                </div>
            </div>
        `;
    });
    
    logsContainer.innerHTML = html;
}

/**
 * Clear logs
 */
function clearLogs() {
    if (!confirm('Are you sure you want to clear all logs?')) {
        return;
    }

    fetch('/api/logs/clear', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('logsContainer').innerHTML = 
                '<p class="empty-state">No logs yet. Start sending emails to see activity here.</p>';
            document.getElementById('sentCount').textContent = '0';
            document.getElementById('failedCount').textContent = '0';
            showToast('Logs cleared', 'success');
        }
    })
    .catch(error => {
        showToast('Error clearing logs: ' + error.message, 'error');
    });
}

/**
 * Update status indicator
 */
function updateStatusIndicator(status) {
    const indicator = document.getElementById('statusIndicator');
    const dot = indicator.querySelector('.status-dot');
    const text = indicator.querySelector('.status-text');
    
    dot.className = 'status-dot';
    
    if (status === 'sending') {
        dot.classList.add('sending');
        text.textContent = 'Sending...';
    } else if (status === 'error') {
        dot.classList.add('error');
        text.textContent = 'Error';
    } else {
        text.textContent = 'Ready';
    }
}

/**
 * Show toast notification with liquid glass effect
 */
function showToast(message, type = 'info') {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast-glass');
    existingToasts.forEach(toast => toast.remove());
    
    // Create new toast with liquid glass effect
    const toast = document.createElement('div');
    toast.className = `toast-glass ${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    else if (type === 'error') icon = 'fa-exclamation-circle';
    else if (type === 'warning') icon = 'fa-exclamation-triangle';
    
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

/**
 * Show completion notification with liquid glass effect
 */
function showCompletionNotification(sent, failed, total) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'completion-overlay';
    
    // Create notification card with liquid glass effect
    const notification = document.createElement('div');
    notification.className = 'completion-notification glass-effect';
    
    const successRate = total > 0 ? Math.round((sent / total) * 100) : 0;
    
    notification.innerHTML = `
        <div class="completion-icon">
            <i class="fas fa-check-circle"></i>
        </div>
        <h2>Email Campaign Complete!</h2>
        <div class="completion-stats">
            <div class="stat-item">
                <div class="stat-number">${total}</div>
                <div class="stat-label">Total Emails</div>
            </div>
            <div class="stat-item success">
                <div class="stat-number">${sent}</div>
                <div class="stat-label">Successfully Sent</div>
            </div>
            <div class="stat-item failed">
                <div class="stat-number">${failed}</div>
                <div class="stat-label">Failed</div>
            </div>
        </div>
        <div class="completion-rate">
            <div class="rate-label">Success Rate</div>
            <div class="rate-bar">
                <div class="rate-fill" style="width: ${successRate}%"></div>
            </div>
            <div class="rate-percentage">${successRate}%</div>
        </div>
        <button class="btn-close-completion" onclick="closeCompletionNotification()">
            <i class="fas fa-times"></i> Close
        </button>
    `;
    
    overlay.appendChild(notification);
    document.body.appendChild(overlay);
    
    // Animate in
    setTimeout(() => {
        overlay.classList.add('active');
        notification.classList.add('active');
    }, 10);
}

/**
 * Close completion notification
 */
function closeCompletionNotification() {
    const overlay = document.querySelector('.completion-overlay');
    if (overlay) {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 300);
    }
}

// Auto-load logs when navigating to logs section
document.addEventListener('DOMContentLoaded', function() {
    const logsNavItem = document.querySelector('[data-section="logs"]');
    if (logsNavItem) {
        logsNavItem.addEventListener('click', loadLogs);
    }
});
