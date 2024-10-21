document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('searchBar');
    const sortOptions = document.getElementById('sortOptions');
    const itemList = document.getElementById('itemList');
    const paginationControls = document.getElementById('paginationControls');
    const itemsPerPage = 10;
    let currentPage = 1;
    let totalPages = 1;

    function filterItems() {
        const filter = searchBar.value.toLowerCase();
        const listItems = itemList.getElementsByClassName('list-item');
        let visibleItems = 0;

        for (let i = 0; i < listItems.length; i++) {
            const itemText = listItems[i].innerText.toLowerCase();
            if (itemText.includes(filter)) {
                listItems[i].style.display = '';
                visibleItems++;
            } else {
                listItems[i].style.display = 'none';
            }
        }

        totalPages = Math.ceil(visibleItems / itemsPerPage);
        updatePagination();
    }

    function sortItems() {
        const sortOption = sortOptions.value;
        const listItems = Array.from(itemList.getElementsByClassName('list-item'));

        listItems.sort((a, b) => {
            const aValue = a.querySelector(`.${sortOption}`).innerText.toLowerCase();
            const bValue = b.querySelector(`.${sortOption}`).innerText.toLowerCase();
            return aValue.localeCompare(bValue);
        });

        itemList.innerHTML = '';
        listItems.forEach(item => itemList.appendChild(item));
        updatePagination();
    }

    function updatePagination() {
        const listItems = Array.from(itemList.getElementsByClassName('list-item')).filter(item => item.style.display !== 'none');
        totalPages = Math.ceil(listItems.length / itemsPerPage);

        for (let i = 0; i < listItems.length; i++) {
            if (i >= (currentPage - 1) * itemsPerPage && i < currentPage * itemsPerPage) {
                listItems[i].style.display = '';
            } else {
                listItems[i].style.display = 'none';
            }
        }

        renderPaginationControls();
    }

    function renderPaginationControls() {
        paginationControls.innerHTML = '';

        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.innerText = i;
            pageButton.classList.add('page-button');
            if (i === currentPage) {
                pageButton.classList.add('active');
            }
            pageButton.addEventListener('click', function() {
                currentPage = i;
                updatePagination();
            });
            paginationControls.appendChild(pageButton);
        }
    }

    searchBar.addEventListener('keyup', filterItems);
    sortOptions.addEventListener('change', sortItems);
    updatePagination();
});