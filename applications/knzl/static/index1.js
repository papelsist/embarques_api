document.addEventListener("DOMContentLoaded",(event)=>{
    if(openScript){
      results.innerHTML = ""
    }
    
})

let openScript;
let results = document.getElementById("results")
let form = document.querySelector('form');
let editor_knzl = document.getElementById("editor_knzl");
let buttonSave = document.getElementById("button-save")
let buttonOpen = document.getElementById("button-open")
let buttonClear = document.getElementById("button-clear")
let buttonClean = document.getElementById("button-clean")

require.config({
    paths: {
        'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.34.1/min/vs'
    }
});

let editor_var = null;

require(['vs/editor/editor.main'], function() {
            // Crear una instancia del editor
            var editor = monaco.editor.create(document.getElementById('editor'), {
                value: editor_knzl.value, // Contenido inicial del editor
                language: "python", // Lenguaje de programación
                theme: "vs", // Tema oscuro
                automaticLayout: true // Ajuste automático del tamaño
            });

            editor_var = editor;    

            // Escuchar cambios en el contenido
            editor.onDidChangeModelContent(function() {
                editor_knzl.value = editor.getValue();
            });
        }); 


editor_knzl.addEventListener("keydown", function(event) {
  if (event.key === "Tab") {
    event.preventDefault(); 
    let start = this.selectionStart;
    console.log("Start",start)
    let end = this.selectionEnd;
    console.log("End",end)
    this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
    console.log("Value",this.value)
    this.selectionStart = this.selectionEnd = start + 1;
    console.log("SS",this,this.selectionStart)
  }
});



buttonSave.addEventListener("click",(e)=>{
  console.log("Salvando Script")
  Swal.fire({
    title: 'Script Name',
    input: 'text',
    inputAttributes: {
      autocapitalize: 'off'
    },
    showCancelButton: true,
    confirmButtonText: 'Save',
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      const name = `${result.value}`
      const content = editor_knzl.value;
      console.log("Name",name)
      const blob = new Blob([content], { type: 'text/plain' });
      const anchor = document.createElement('a');
      anchor.download = `${name}.py`;
      anchor.href = URL.createObjectURL(blob);
      anchor.click();

    }
  })
}) 


buttonOpen.addEventListener("click",(e)=>{
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.py'; 
  input.onchange = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
        const content = e.target.result;
        editor_knzl.value = content;
        editor_var.setValue(content);
    };
    reader.readAsText(file);
  };
  input.click();
})



form.addEventListener('submit', function(e) {
    results.innerText = "";
    let loader = document.getElementById('loader');
    loader.style.display = 'block'; 
});

buttonClear.addEventListener('click', function() {
  results.innerText = "";
  });

buttonClean.addEventListener('click', function() {
    
  Swal.fire({
    title: 'Clean Editor?',
    showCancelButton: true,
    confirmButtonText: 'Accept',
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      editor_knzl.value = "";
      editor_var.setValue("");
    }
  })
  }); 



