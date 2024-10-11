let input = document.getElementById("todo-input");
let addTask = document.getElementById("add-task-btn");
let TasksList = document.getElementById("todo-list");

let Tasks = [];

// after clicking on add task button this happens
addTask.addEventListener("click", () => {
  const taskText = input.value.trim();
  if (taskText === "false") return;

  const newTask = {
    id: Date.now(),
    text: taskText,
    completed: false,
  };
  Tasks.push(newTask); // add the input into the array Tasks
  saveTasks(); // we are saving the tasks in localStorage
  input.value = ""; // clearing the input once it is saved
  // console.log(Tasks);
});

function saveTasks() {
  localStorage.setItem("Tasks", JSON.stringify(Tasks));
}
