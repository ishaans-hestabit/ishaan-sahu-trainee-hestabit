let todos = JSON.parse(localStorage.getItem('my-todos')) || [];

function renderTodo(){
    let todo_box = document.querySelector('.todo-lists');
    todo_box.innerHTML = "";
    
    todos.forEach((todo) => {
        // list item created
        let todo_li = document.createElement('li');
        
        // span added to add text of todo
        let todo_text = document.createElement('span');
        todo_text.textContent = todo.value;

        todo_box.appendChild(todo_li);
        todo_li.appendChild(todo_text);

        // edit button created and functionality is added
        let edit_button = document.createElement('button');
        edit_button.textContent = "Edit";
        edit_button.className = "edit-btn";
        edit_button.dataset.id = todo.id;

        edit_button.addEventListener("click",(event)=>{

            let new_todo_content = prompt("Edit Todo");

            if (new_todo_content !== null && new_todo_content.trim().length > 0) {
                    let updated_todos = todos.map((todo)=>{
                                                    if(todo.id === Number(edit_button.dataset.id)){
                                                        todo.value = new_todo_content;
                                                    }
                                                    return todo;
                                                });
                                        todos = updated_todos;
                                        localStorage.setItem('my-todos',JSON.stringify(todos));
                    }
            renderTodo();
        });

        todo_li.appendChild(edit_button);


        // delete button creadted and delete functionality is added
        let delete_button = document.createElement('button');
        delete_button.dataset.id = todo.id;
        delete_button.textContent = 'Delete';
        delete_button.className = "delete-btn";

        delete_button.addEventListener("click",(event)=>{
           let updated_todos = todos.filter((todo)=>{
            return todo.id != Number(delete_button.dataset.id);
           })
           todos = updated_todos;
           localStorage.setItem('my-todos',JSON.stringify(todos));
           renderTodo()
        });
        todo_li.appendChild(delete_button);

        
        
    });
}

document.querySelector('.todo-form').addEventListener("submit",(event)=>{
    event.preventDefault();
    let todo = document.querySelector('.todo-input');

    // this prevents empty todo adding
    if(todo.value.trim().length == 0) return;
    // Date.now() gives times in miliseconds after 1 Jan 1970
    todos.push({id: Date.now(),value : todo.value, status: 'not-completed'});

    localStorage.setItem('my-todos',JSON.stringify(todos));
    todo.value = "";
    console.log(todos);
    renderTodo(todos);
}); 

// this is because if there are todos already in local storage and the page reloads so we should render the initial ones first
renderTodo()