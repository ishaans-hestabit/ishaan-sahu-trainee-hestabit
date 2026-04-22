
    const todoInput = document.getElementById('todo-input');
    const addTodoBtn = document.getElementById('add-todo-btn');
    const todoList = document.getElementById('todo-list');

    addTodoBtn.addEventListener('click', () => {
        const todoItem = todoInput.value;
        if (todoItem !== '') {
            const li = document.createElement('li');
            li.textContent = todoItem;
            todoList.appendChild(li);
            todoInput.value = '';
        }
    });
    