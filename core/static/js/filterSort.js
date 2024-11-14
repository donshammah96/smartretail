document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('searchBar');
    const sortOptions = document.getElementById('sortOptions');
    const itemList = document.getElementById('itemList');
    const items = Array.from(itemList.getElementsByClassName('list-item'));

    searchBar.addEventListener('keyup', filterItems);
    sortOptions.addEventListener('change', sortItems);

    function filterItems() {
        const searchText = searchBar.value.toLowerCase();
        items.forEach(function(item) {
            const itemName = item.querySelector('.item-details p strong').nextSibling.textContent.toLowerCase();
            if (itemName.includes(searchText)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }

    function sortItems() {
        const sortBy = sortOptions.value;
        const sortedItems = items.sort(function(a, b) {
            const aValue = a.querySelector(`.item-details p strong:contains(${sortBy})`).nextSibling.textContent.toLowerCase();
            const bValue = b.querySelector(`.item-details p strong:contains(${sortBy})`).nextSibling.textContent.toLowerCase();
            if (aValue < bValue) return -1;
            if (aValue > bValue) return 1;
            return 0;
        });
        sortedItems.forEach(function(item) {
            itemList.appendChild(item);
        });
    }
});