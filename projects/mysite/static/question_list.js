document.addEventListener('DOMContentLoaded', () => {
	const searchInput = document.getElementById('search-input');
	const searchSelect = document.getElementById('search-select');
	const searchButton = document.getElementById('search-button');

	const pageLinks = document.getElementsByClassName('page-link');
	
	const searchOrders = document.getElementsByClassName('search-order');

	const searchForm = document.getElementById('search-form');
	const page = document.getElementById('page');
	const kw = document.getElementById('kw');
	const st = document.getElementById('st');
	const so = document.getElementById('so');

	function getQueryParam(name) {
		const urlParams = new URLSearchParams(window.location.search);
		return urlParams.get(name);
	}

	const searchType = getQueryParam('st');
	if (searchType) {
		searchSelect.value = searchType;
	} else {
		searchSelect.value = 'title';
	}

	Array.from(pageLinks).forEach(link => {
		link.addEventListener('click', (event) => {
			event.preventDefault();
			so.value = so.value;
			kw.value = searchInput.value;
			st.value = searchSelect.value;
			page.value = link.dataset.page;
			searchForm.submit();
		});
	});

	searchButton.addEventListener('click', () => {
		kw.value = searchInput.value;
		st.value = searchSelect.value;
		page.value = 1;
		searchForm.submit();
	});

	searchOrder = getQueryParam('so');
	if (searchOrder) {
		so.value = searchOrder;
	} else {
		so.value = 'recent';
		searchOrder = 'recent';
	}
	
	Array.from(searchOrders).forEach(btn => {
		btn.addEventListener('click', (event) => {
			event.preventDefault();
			so.value = btn.dataset.so;
			kw.value = searchInput.value;
			st.value = searchSelect.value;
			page.value = 1;
			searchForm.submit();
		});
		if (btn.dataset.so === searchOrder) {
			btn.classList.add('selected');
		}
	});

});