    document.querySelector('.expand-button').addEventListener('click', function() {
    const taskList = document.getElementById('task-list');
    if (taskList.style.display === 'none' || taskList.style.display === '') {
        taskList.style.display = 'block';
        this.textContent = 'свернуть'; // Change button text to "свернуть"
    } else {
        taskList.style.display = 'none';
        this.textContent = 'развернуть'; // Change button text back to "развернуть"
    }
});

