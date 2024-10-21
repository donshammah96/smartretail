document.addEventListener('DOMContentLoaded', function() {
    let currentPage = 1;
    const itemsPerPage = 5;
    let totalPages = 1;

    // Filter items by name
    function filterItems() {
        const searchBar = document.getElementById('searchBar');
        const filter = searchBar.value.toLowerCase();
        const listItems = document.getElementsByClassName('list-item');

        for (let i = 0; i < listItems.length; i++) {
            const itemName = listItems[i].getElementsByClassName('item-details')[0].getElementsByTagName('p')[0].innerText.toLowerCase();
            if (itemName.includes(filter)) {
                listItems[i].style.display = '';
            } else {
                listItems[i].style.display = 'none';
            }
        }
        updatePagination();
    }

    // Sort items
    function sortItems() {
        const sortOptions = document.getElementById('sortOptions').value;
        const itemList = document.getElementById('itemList');
        const listItems = Array.from(itemList.getElementsByClassName('list-item'));

        listItems.sort((a, b) => {
            const aValue = a.getElementsByClassName('item-details')[0].getElementsByTagName('p')[sortOptions === 'name' ? 0 : 1].innerText.toLowerCase();
            const bValue = b.getElementsByClassName('item-details')[0].getElementsByTagName('p')[sortOptions === 'name' ? 0 : 1].innerText.toLowerCase();
            return aValue.localeCompare(bValue);
        });

        itemList.innerHTML = '';
        listItems.forEach(item => itemList.appendChild(item));
        updatePagination();
    }

    // Toggle item details
    function toggleDetails(button) {
        const details = button.previousElementSibling;
        if (details.style.display === 'none' || details.style.display === '') {
            details.style.display = 'block';
        } else {
            details.style.display = 'none';
        }
    }

    // Update pagination
    function updatePagination() {
        const listItems = Array.from(document.getElementsByClassName('list-item'));
        const visibleItems = listItems.filter(item => item.style.display !== 'none');
        totalPages = Math.ceil(visibleItems.length / itemsPerPage);

        for (let i = 0; i < visibleItems.length; i++) {
            if (i >= (currentPage - 1) * itemsPerPage && i < currentPage * itemsPerPage) {
                visibleItems[i].style.display = '';
            } else {
                visibleItems[i].style.display = 'none';
            }
        }

        renderPaginationControls();
    }

    // Render pagination controls
    function renderPaginationControls() {
        const paginationControls = document.getElementById('paginationControls');
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

    // Attach event listeners
    document.getElementById('searchBar').addEventListener('keyup', filterItems);
    document.getElementById('sortOptions').addEventListener('change', sortItems);
    const toggleButtons = document.getElementsByClassName('toggle-button');
    for (let i = 0; i < toggleButtons.length; i++) {
        toggleButtons[i].addEventListener('click', function() {
            toggleDetails(this);
        });
    }

    // Initial pagination setup
    updatePagination();
});