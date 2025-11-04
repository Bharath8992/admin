// Main JavaScript for common functionality

// Mobile sidebar toggle for all pages
document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleSidebar');
    const sidebar = document.querySelector('.sidebar');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            sidebar.classList.toggle('show');
            
            // Add overlay when sidebar is open
            if (sidebar.classList.contains('show')) {
                const overlay = document.createElement('div');
                overlay.id = 'sidebarOverlay';
                overlay.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.5);
                    z-index: 999;
                    backdrop-filter: blur(2px);
                `;
                
                overlay.addEventListener('click', function() {
                    sidebar.classList.remove('show');
                    overlay.remove();
                    document.body.style.overflow = '';
                });
                
                document.body.appendChild(overlay);
                document.body.style.overflow = 'hidden';
            } else {
                const overlay = document.getElementById('sidebarOverlay');
                if (overlay) {
                    overlay.remove();
                    document.body.style.overflow = '';
                }
            }
        });
        
        // Close sidebar when clicking on links (mobile)
        const navLinks = sidebar.querySelectorAll('.nav-link-compact');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 991) {
                    sidebar.classList.remove('show');
                    const overlay = document.getElementById('sidebarOverlay');
                    if (overlay) {
                        overlay.remove();
                        document.body.style.overflow = '';
                    }
                }
            });
        });
    }
    
    // Close sidebar on window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 991 && sidebar) {
            sidebar.classList.remove('show');
            const overlay = document.getElementById('sidebarOverlay');
            if (overlay) {
                overlay.remove();
                document.body.style.overflow = '';
            }
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar on mobile
    const toggleBtn = document.getElementById("toggleSidebar");
    const sidebar = document.querySelector("aside.sidebar");
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", ()=> {
            if(sidebar.style.display==="none" || getComputedStyle(sidebar).display==="none"){
                sidebar.style.display="block";
            } else {
                sidebar.style.display="none";
            }
        });
    }

    // Form submissions for auth pages
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            // Simple validation
            if (!email || !password) {
                alert('Please fill in all fields');
                return;
            }
            
            // Simulate login process
            alert('Login successful! Redirecting to dashboard...');
            window.location.href = 'index.html';
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('registerName').value;
            const email = document.getElementById('registerEmail').value;
            const phone = document.getElementById('registerPhone').value;
            const password = document.getElementById('registerPassword').value;
            const confirmPassword = document.getElementById('registerConfirmPassword').value;
            
            // Validation
            if (!name || !email || !phone || !password || !confirmPassword) {
                alert('Please fill in all fields');
                return;
            }
            
            if (password !== confirmPassword) {
                alert('Passwords do not match');
                return;
            }
            
            // Simulate registration process
            alert('Registration successful! Please login.');
            window.location.href = 'login.html';
        });
    }

    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('forgotEmail').value;
            
            if (!email) {
                alert('Please enter your email');
                return;
            }
            
            // Simulate password reset process
            alert('Password reset link sent to your email!');
            window.location.href = 'login.html';
        });
    }

    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if(confirm('Are you sure you want to logout?')) {
                alert('You have been logged out');
                window.location.href = 'login.html';
            }
        });
    }
});