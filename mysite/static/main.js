
document.addEventListener('DOMContentLoaded', () => {
	const menuButton = document.getElementById('menuButton');
	const menu = document.getElementById('menu');

	menuButton.addEventListener('click', () => {
		menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
	});
});
