
document.addEventListener('DOMContentLoaded', () => {
	const menuButton = document.getElementById('toggleBtn');
	const bg = document.getElementById('bg');
	const navBg = document.getElementById('nav-bg');
	const report = document.getElementById('menu-report');
	const mobileOnly = document.getElementById('mobile-only');

	if (window.innerWidth > 768) {
		bg.style.display = 'flex';
	}

	menuButton.addEventListener('click', () => {
		bg.style.display = 'flex';
		mobileOnly.style.display = 'flex';
		report.style.display = 'none';
	});
	
	navBg.addEventListener('click', () => {
		bg.style.display = 'none';
		mobileOnly.style.display = 'none';
		report.style.display = 'block';
	});
});
