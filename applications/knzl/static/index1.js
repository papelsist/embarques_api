document.addEventListener("DOMContentLoaded",(event)=>{
    if(openScript){
      results.innerHTML = ""
    }
    
    // Initialize script tree
    renderScriptTree();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Add visual feedback for buttons
    addButtonFeedback();
    
    // Initialize language system
    langManager.updateUI();
    
    // Theme switcher event listener
    document.getElementById('theme-toggle').addEventListener('click', () => {
        themeManager.toggleTheme();
    });
    
    // Language switcher event listeners
    document.getElementById('lang-en').addEventListener('click', () => {
        langManager.setLanguage('en');
        updateLanguageButtons();
    });
    
    document.getElementById('lang-es').addEventListener('click', () => {
        langManager.setLanguage('es');
        updateLanguageButtons();
    });
    
    // Initialize language buttons
    updateLanguageButtons();
    
    // Add console welcome message if results are empty
    if (!results.innerHTML.trim()) {
        const colors = themeManager.getConsoleColors();
        results.innerHTML = `<pre style="color: ${colors.primary};">${langManager.t('welcomeMessage')}</pre>`;
    }
})

// Keyboard shortcuts
function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + R to run code
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            form.submit();
        }
        
        // Ctrl/Cmd + S to save to local storage
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            buttonSaveLocal.click();
        }
        
        // Ctrl/Cmd + O to open file
        if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
            e.preventDefault();
            buttonOpen.click();
        }
        
        // Ctrl/Cmd + K to clear output
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            buttonClear.click();
        }
        
        // Escape to deselect scripts
        if (e.key === 'Escape') {
            document.querySelectorAll('.script-item').forEach(item => {
                item.classList.remove('selected');
            });
            scriptStorage.selectedScriptId = null;
        }
    });
}

let openScript;
let results = document.getElementById("results")
let form = document.querySelector('form');
let editor_knzl = document.getElementById("editor_knzl");
let buttonSave = document.getElementById("button-save")
let buttonOpen = document.getElementById("button-open")
let buttonClear = document.getElementById("button-clear")
let buttonClean = document.getElementById("button-clean")
let buttonSaveLocal = document.getElementById("button-save-local")
let buttonRefreshScripts = document.getElementById("button-refresh-scripts")
let buttonClearStorage = document.getElementById("button-clear-storage")
let scriptTree = document.getElementById("script-tree")
let noScriptsMessage = document.getElementById("no-scripts-message")
let scriptSearch = document.getElementById("script-search")

// Local Storage Manager
class ScriptStorage {
    constructor() {
        this.storageKey = 'knzl_scripts';
        this.selectedScriptId = null;
    }
    
    saveScript(name, content) {
        const scripts = this.getAllScripts();
        const id = this.generateId();
        const script = {
            id: id,
            name: name,
            content: content,
            created: new Date().toISOString(),
            modified: new Date().toISOString()
        };
        
        // Check if script with same name exists
        const existingIndex = scripts.findIndex(s => s.name === name);
        if (existingIndex !== -1) {
            script.id = scripts[existingIndex].id;
            script.created = scripts[existingIndex].created;
            scripts[existingIndex] = script;
        } else {
            scripts.push(script);
        }
        
        this.saveAllScripts(scripts);
        return script;
    }
    
    getAllScripts() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : [];
    }
    
    saveAllScripts(scripts) {
        localStorage.setItem(this.storageKey, JSON.stringify(scripts));
    }
    
    getScript(id) {
        const scripts = this.getAllScripts();
        return scripts.find(s => s.id === id);
    }
    
    deleteScript(id) {
        const scripts = this.getAllScripts();
        const filtered = scripts.filter(s => s.id !== id);
        this.saveAllScripts(filtered);
    }
    
    clearAllScripts() {
        localStorage.removeItem(this.storageKey);
    }
    
    generateId() {
        return 'script_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
}

const scriptStorage = new ScriptStorage();

// Language System
class LanguageManager {
    constructor() {
        this.currentLang = localStorage.getItem('knzl_language') || 'en';
        this.translations = {
            en: {
                title: 'DJANGO-KNZL-SHELL',
                run: 'Run',
                saveFile: 'Save File',
                openFile: 'Open File',
                saveStorage: 'Save to Storage',
                clearOutput: 'Clear Output',
                cleanEditor: 'Clean Editor',
                scripts: 'Scripts',
                clearAll: 'Clear All',
                shortcuts: 'Shortcuts:',
                shortcutRun: 'Run',
                shortcutSave: 'Save',
                shortcutOpen: 'Open',
                shortcutClear: 'Clear',
                shortcutDeselect: 'Deselect',
                consoleOutput: 'Console Output',
                searchScripts: 'Search scripts...',
                noScripts: 'No scripts stored yet.',
                noScriptsFound: 'No scripts found matching',
                welcomeMessage: `Django KNZL Shell v1.0
Welcome to the interactive Django Python shell.
Type your Python code and press Ctrl+R or click Run to execute.

Ready for input...`,
                executingCode: 'Executing code...',
                outputCleared: 'Output cleared.',
                cleanEditor: 'Clean Editor?',
                accept: 'Accept',
                scriptName: 'Script Name',
                enterScriptName: 'Enter script name...',
                scriptSaved: 'Script Saved!',
                savedToStorage: 'saved to local storage',
                scriptsRefreshed: 'Scripts Refreshed',
                emptyScript: 'Empty Script',
                cannotSaveEmpty: 'Cannot save empty script!',
                deleteScript: 'Delete Script?',
                sureToDelete: 'Are you sure you want to delete',
                cannotBeUndone: 'This action cannot be undone.',
                yesDelete: 'Yes, delete it!',
                deleted: 'Deleted!',
                hasBeenDeleted: 'has been deleted.',
                clearAllScripts: 'Clear All Scripts?',
                deleteAllScripts: 'This will delete all',
                savedScripts: 'saved scripts. This action cannot be undone!',
                yesClearAll: 'Yes, clear all!',
                cleared: 'Cleared!',
                allScriptsDeleted: 'All scripts have been deleted.',
                loadScript: 'Load Script',
                deleteScript: 'Delete Script',
                scriptLoaded: 'Script Loaded',
                loadedSuccessfully: 'loaded successfully',
                executionCompleted: 'Execution completed',
                fileSavedSuccessfully: 'saved successfully',
                fileDownloadedTo: 'downloaded to default folder',
                failedToSaveFile: 'Failed to save file',
                failedToOpenFile: 'Failed to open file',
                failedToReadFile: 'Failed to read file',
                cancel: 'Cancel',
                noOutput: 'No output',
                executionError: 'Execution error',
                checkConsole: 'Please try again or check the console for more details.',
                executing: 'Executing...'
            },
            es: {
                title: 'DJANGO-KNZL-SHELL',
                run: 'Ejecutar',
                saveFile: 'Guardar Archivo',
                openFile: 'Abrir Archivo',
                saveStorage: 'Guardar en Storage',
                clearOutput: 'Limpiar Salida',
                cleanEditor: 'Limpiar Editor',
                scripts: 'Scripts',
                clearAll: 'Limpiar Todo',
                shortcuts: 'Atajos:',
                shortcutRun: 'Ejecutar',
                shortcutSave: 'Guardar',
                shortcutOpen: 'Abrir',
                shortcutClear: 'Limpiar',
                shortcutDeselect: 'Deseleccionar',
                consoleOutput: 'Salida de Consola',
                searchScripts: 'Buscar scripts...',
                noScripts: 'No hay scripts guardados aún.',
                noScriptsFound: 'No se encontraron scripts que coincidan con',
                welcomeMessage: `Django KNZL Shell v1.0
Bienvenido al shell interactivo de Django Python.
Escribe tu código Python y presiona Ctrl+R o haz clic en Ejecutar.

Listo para entrada...`,
                executingCode: 'Ejecutando código...',
                outputCleared: 'Salida limpiada.',
                cleanEditor: '¿Limpiar Editor?',
                accept: 'Aceptar',
                scriptName: 'Nombre del Script',
                enterScriptName: 'Ingresa el nombre del script...',
                scriptSaved: '¡Script Guardado!',
                savedToStorage: 'guardado en el almacenamiento local',
                scriptsRefreshed: 'Scripts Actualizados',
                emptyScript: 'Script Vacío',
                cannotSaveEmpty: '¡No se puede guardar un script vacío!',
                deleteScript: '¿Eliminar Script?',
                sureToDelete: '¿Estás seguro de que quieres eliminar',
                cannotBeUndone: 'Esta acción no se puede deshacer.',
                yesDelete: 'Sí, eliminarlo!',
                deleted: '¡Eliminado!',
                hasBeenDeleted: 'ha sido eliminado.',
                clearAllScripts: '¿Limpiar Todos los Scripts?',
                deleteAllScripts: 'Esto eliminará todos los',
                savedScripts: 'scripts guardados. ¡Esta acción no se puede deshacer!',
                yesClearAll: 'Sí, limpiar todo!',
                cleared: '¡Limpiado!',
                allScriptsDeleted: 'Todos los scripts han sido eliminados.',
                loadScript: 'Cargar Script',
                deleteScript: 'Eliminar Script',
                scriptLoaded: 'Script Cargado',
                loadedSuccessfully: 'cargado exitosamente',
                executionCompleted: 'Ejecución completada',
                fileSavedSuccessfully: 'guardado exitosamente',
                fileDownloadedTo: 'descargado en la carpeta predeterminada',
                failedToSaveFile: 'Error al guardar archivo',
                failedToOpenFile: 'Error al abrir archivo',
                failedToReadFile: 'Error al leer archivo',
                cancel: 'Cancelar',
                noOutput: 'Sin salida',
                executionError: 'Error de ejecución',
                checkConsole: 'Por favor intenta de nuevo o revisa la consola para más detalles.',
                executing: 'Ejecutando...'
            }
        };
    }
    
    setLanguage(lang) {
        this.currentLang = lang;
        localStorage.setItem('knzl_language', lang);
        this.updateUI();
    }
    
    t(key) {
        return this.translations[this.currentLang][key] || this.translations['en'][key] || key;
    }
    
    updateUI() {
        // Update button texts
        document.querySelector('button[type="submit"]').innerHTML = `<i class="fas fa-play"></i> ${this.t('run')}`;
        document.getElementById('button-save').innerHTML = `<i class="fas fa-download"></i> ${this.t('saveFile')}`;
        document.getElementById('button-open').innerHTML = `<i class="fas fa-folder-open"></i> ${this.t('openFile')}`;
        document.getElementById('button-save-local').innerHTML = `<i class="fas fa-save"></i> ${this.t('saveStorage')}`;
        document.getElementById('button-clear').innerHTML = `<i class="fas fa-eraser"></i> ${this.t('clearOutput')}`;
        document.getElementById('button-clean').innerHTML = `<i class="fas fa-trash"></i> ${this.t('cleanEditor')}`;
        document.getElementById('button-clear-storage').innerHTML = `<i class="fas fa-trash-alt"></i> ${this.t('clearAll')}`;
        
        // Update panel headers
        document.querySelector('.panel-header h5').innerHTML = `<i class="fas fa-code-branch"></i> ${this.t('scripts')} <button class="btn btn-sm btn-outline-light float-end" id="button-refresh-scripts"><i class="fas fa-sync-alt"></i></button>`;
        document.querySelector('.results-header').innerHTML = `<i class="fas fa-terminal"></i> ${this.t('consoleOutput')}`;
        
        // Update search placeholder
        document.getElementById('script-search').placeholder = this.t('searchScripts');
        
        // Update shortcuts
        const shortcutsDiv = document.querySelector('.keyboard-shortcuts');
        shortcutsDiv.innerHTML = `
            <strong>${this.t('shortcuts')}</strong><br>
            <kbd>Ctrl+R</kbd> ${this.t('shortcutRun')}<br>
            <kbd>Ctrl+S</kbd> ${this.t('shortcutSave')}<br>
            <kbd>Ctrl+O</kbd> ${this.t('shortcutOpen')}<br>
            <kbd>Ctrl+K</kbd> ${this.t('shortcutClear')}<br>
            <kbd>Esc</kbd> ${this.t('shortcutDeselect')}
        `;
        
        // Update welcome message if results are empty or contain welcome
        const resultsContent = results.innerHTML;
        if (!resultsContent.trim() || resultsContent.includes('Django KNZL Shell v1.0')) {
            const colors = themeManager.getConsoleColors();
            results.innerHTML = `<pre style="color: ${colors.primary};">${this.t('welcomeMessage')}</pre>`;
        }
        
        // Re-render script tree to update messages
        renderScriptTree();
    }
}

const langManager = new LanguageManager();

// Theme Manager
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('knzl_theme') || 'dark';
        this.applyTheme();
    }
    
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('knzl_theme', this.currentTheme);
        this.applyTheme();
        this.updateMonacoTheme();
    }
    
    applyTheme() {
        const body = document.body;
        if (this.currentTheme === 'light') {
            body.setAttribute('data-theme', 'light');
        } else {
            body.removeAttribute('data-theme');
        }
        
        this.updateThemeIcon();
    }
    
    updateThemeIcon() {
        const icon = document.getElementById('theme-icon');
        const button = document.getElementById('theme-toggle');
        
        if (this.currentTheme === 'light') {
            icon.className = 'fas fa-sun';
            button.title = 'Switch to Dark Theme';
        } else {
            icon.className = 'fas fa-moon';
            button.title = 'Switch to Light Theme';
        }
    }
    
    updateMonacoTheme() {
        if (editor_var) {
            const monacoTheme = this.currentTheme === 'light' ? 'vs' : 'vs-dark';
            monaco.editor.setTheme(monacoTheme);
        }
    }
    
    getConsoleColors() {
        if (this.currentTheme === 'light') {
            return {
                primary: '#28a745',
                secondary: '#ffc107',
                background: '#ffffff'
            };
        } else {
            return {
                primary: '#00ff00',
                secondary: '#ffff00',
                background: '#0c0c0c'
            };
        }
    }
}

const themeManager = new ThemeManager();

// Auto-scroll function for results
function scrollToBottom() {
    const scrollWrapper = document.querySelector('.results-scroll-wrapper');
    if (scrollWrapper) {
        scrollWrapper.scrollTop = scrollWrapper.scrollHeight;
    }
}

// Update language button states
function updateLanguageButtons() {
    document.getElementById('lang-en').classList.toggle('active', langManager.currentLang === 'en');
    document.getElementById('lang-es').classList.toggle('active', langManager.currentLang === 'es');
}

// Script Tree Renderer
function renderScriptTree(searchTerm = '') {
    const scripts = scriptStorage.getAllScripts();
    scriptTree.innerHTML = '';
    
    // Filter scripts based on search term
    const filteredScripts = searchTerm ? 
        scripts.filter(script => 
            script.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            script.content.toLowerCase().includes(searchTerm.toLowerCase())
        ) : scripts;
    
    if (filteredScripts.length === 0) {
        const message = searchTerm ? 
            `${langManager.t('noScriptsFound')} "${searchTerm}"` : 
            langManager.t('noScripts');
        noScriptsMessage.textContent = message;
        noScriptsMessage.style.display = 'block';
        scriptTree.appendChild(noScriptsMessage);
        return;
    }
    
    noScriptsMessage.style.display = 'none';
    
    // Sort scripts by modification date (newest first)
    filteredScripts.sort((a, b) => new Date(b.modified) - new Date(a.modified));
    
    filteredScripts.forEach(script => {
        const scriptElement = createScriptElement(script);
        scriptTree.appendChild(scriptElement);
    });
}

function createScriptElement(script) {
    const div = document.createElement('div');
    div.className = 'script-item';
    div.dataset.scriptId = script.id;
    
    const modifiedDate = new Date(script.modified).toLocaleString();
    
    div.innerHTML = `
        <div class="script-actions">
            <button class="btn btn-sm btn-outline-primary load-script" title="${langManager.t('loadScript')}">
                <i class="fas fa-upload"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger delete-script" title="${langManager.t('deleteScript')}">
                <i class="fas fa-trash"></i>
            </button>
        </div>
        <span class="script-name">${script.name}</span>
        <span class="script-date">Modified: ${modifiedDate}</span>
    `;
    
    // Add click event to select script
    div.addEventListener('click', (e) => {
        if (!e.target.closest('.script-actions')) {
            selectScript(script.id);
        }
    });
    
    // Load script button
    div.querySelector('.load-script').addEventListener('click', (e) => {
        e.stopPropagation();
        loadScript(script.id);
    });
    
    // Delete script button
    div.querySelector('.delete-script').addEventListener('click', (e) => {
        e.stopPropagation();
        deleteScriptConfirm(script.id, script.name);
    });
    
    return div;
}

function selectScript(scriptId) {
    // Remove previous selection
    document.querySelectorAll('.script-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // Add selection to current script
    const scriptElement = document.querySelector(`[data-script-id="${scriptId}"]`);
    if (scriptElement) {
        scriptElement.classList.add('selected');
        scriptStorage.selectedScriptId = scriptId;
    }
}

function loadScript(scriptId) {
    const script = scriptStorage.getScript(scriptId);
    if (script) {
        editor_knzl.value = script.content;
        if (editor_var) {
            editor_var.setValue(script.content);
        }
        selectScript(scriptId);
        
        Swal.fire({
            icon: 'success',
            title: langManager.t('scriptLoaded'),
            text: `"${script.name}" ${langManager.t('loadedSuccessfully')}`,
            timer: 2000,
            showConfirmButton: false
        });
    }
}

function deleteScriptConfirm(scriptId, scriptName) {
    Swal.fire({
        title: langManager.t('deleteScript'),
        text: `${langManager.t('sureToDelete')} "${scriptName}"? ${langManager.t('cannotBeUndone')}`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: langManager.t('yesDelete'),
        cancelButtonText: langManager.t('cancel')
    }).then((result) => {
        if (result.isConfirmed) {
            scriptStorage.deleteScript(scriptId);
            renderScriptTree();
            
            Swal.fire({
                icon: 'success',
                title: langManager.t('deleted'),
                text: `"${scriptName}" ${langManager.t('hasBeenDeleted')}`,
                timer: 2000,
                showConfirmButton: false
            });
        }
    });
}

require.config({
    paths: {
        'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.34.1/min/vs'
    }
});

let editor_var = null;

require(['vs/editor/editor.main'], function() {
            // Determinar tema inicial
            const initialTheme = themeManager.currentTheme === 'light' ? 'vs' : 'vs-dark';
            
            // Crear una instancia del editor
            var editor = monaco.editor.create(document.getElementById('editor'), {
                value: editor_knzl.value, // Contenido inicial del editor
                language: "python", // Lenguaje de programación
                theme: initialTheme, // Tema dinámico
                automaticLayout: true, // Ajuste automático del tamaño
                fontSize: 14,
                fontFamily: "'Consolas', 'Monaco', 'Courier New', monospace",
                lineNumbers: 'on',
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                wordWrap: 'on',
                glyphMargin: false,
                folding: false,
                lineDecorationsWidth: 10,
                lineNumbersMinChars: 3,
                renderLineHighlight: 'all',
                scrollbar: {
                    vertical: 'auto',
                    horizontal: 'auto',
                    verticalScrollbarSize: 8,
                    horizontalScrollbarSize: 8
                }
            });

            editor_var = editor;    

            // Escuchar cambios en el contenido
            editor.onDidChangeModelContent(function() {
                editor_knzl.value = editor.getValue();
            });
            
            // Focus the editor on load
            editor.focus();
            
            // Actualizar tema del editor cuando cambie
            themeManager.updateMonacoTheme();
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



// Check if File System Access API is supported
function isFileSystemAccessSupported() {
    return 'showSaveFilePicker' in window;
}

// Save file with location picker (modern browsers)
async function saveFileWithPicker(filename, content) {
    try {
        const fileHandle = await window.showSaveFilePicker({
            suggestedName: filename,
            types: [
                {
                    description: 'Python files',
                    accept: {
                        'text/x-python': ['.py'],
                    },
                },
                {
                    description: 'Text files',
                    accept: {
                        'text/plain': ['.txt'],
                    },
                },
                {
                    description: 'JavaScript files',
                    accept: {
                        'text/javascript': ['.js'],
                    },
                },
                {
                    description: 'JSON files',
                    accept: {
                        'application/json': ['.json'],
                    },
                },
            ],
            excludeAcceptAllOption: false,
        });
        
        const writable = await fileHandle.createWritable();
        await writable.write(content);
        await writable.close();
        
        return true;
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error('Error saving file:', err);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: langManager.t('failedToSaveFile') + ': ' + err.message
            });
        }
        return false;
    }
}

// Fallback save method (legacy browsers)
function saveFileAsDownload(filename, content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const anchor = document.createElement('a');
    anchor.download = filename;
    anchor.href = URL.createObjectURL(blob);
    anchor.click();
    URL.revokeObjectURL(anchor.href);
}

buttonSave.addEventListener("click", async (e) => {
    console.log("Saving Script")
    
    const content = editor_knzl.value.trim();
    
    if (!content) {
        Swal.fire({
            icon: 'warning',
            title: langManager.t('emptyScript'),
            text: langManager.t('cannotSaveEmpty')
        });
        return;
    }
    
    Swal.fire({
        title: langManager.t('scriptName'),
        input: 'text',
        inputLabel: langManager.t('enterScriptName'),
        inputPlaceholder: 'my_script',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: langManager.t('saveFile').split(' ')[0], // Just "Save"
        cancelButtonText: langManager.t('cancel'),
        allowOutsideClick: () => !Swal.isLoading(),
        inputValidator: (value) => {
            if (!value) {
                return langManager.t('enterScriptName').replace('...', '!')
            }
        }
    }).then(async (result) => {
        if (result.isConfirmed) {
            const name = result.value.trim();
            const filename = name.endsWith('.py') ? name : `${name}.py`;
            
            if (isFileSystemAccessSupported()) {
                // Use modern File System Access API
                const saved = await saveFileWithPicker(filename, content);
                if (saved) {
                    Swal.fire({
                        icon: 'success',
                        title: langManager.t('scriptSaved'),
                        text: `"${filename}" ${langManager.t('fileSavedSuccessfully')}`,
                        timer: 2000,
                        showConfirmButton: false
                    });
                }
            } else {
                // Fallback to download method
                saveFileAsDownload(filename, content);
                Swal.fire({
                    icon: 'success',
                    title: langManager.t('scriptSaved'),
                    text: `"${filename}" ${langManager.t('fileDownloadedTo')}`,
                    timer: 2000,
                    showConfirmButton: false
                });
            }
        }
    });
}); 


// Check if File System Access API is supported for opening files
function isFileOpenAccessSupported() {
    return 'showOpenFilePicker' in window;
}

// Open file with file picker (modern browsers)
async function openFileWithPicker() {
    try {
        const [fileHandle] = await window.showOpenFilePicker({
            types: [
                {
                    description: 'Python files',
                    accept: {
                        'text/x-python': ['.py'],
                    },
                },
                {
                    description: 'Text files',
                    accept: {
                        'text/plain': ['.txt'],
                    },
                },
                {
                    description: 'JavaScript files',
                    accept: {
                        'text/javascript': ['.js'],
                    },
                },
                {
                    description: 'JSON files',
                    accept: {
                        'application/json': ['.json'],
                    },
                },
                {
                    description: 'All text files',
                    accept: {
                        'text/*': ['.py', '.txt', '.js', '.json', '.md', '.html', '.css', '.xml', '.csv'],
                    },
                },
            ],
            multiple: false,
            excludeAcceptAllOption: false,
        });
        
        const file = await fileHandle.getFile();
        const content = await file.text();
        
        return { content, filename: file.name };
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error('Error opening file:', err);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: langManager.t('failedToOpenFile') + ': ' + err.message
            });
        }
        return null;
    }
}

// Fallback open method (legacy browsers)
function openFileAsInput() {
    return new Promise((resolve) => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.py,.txt,.js,.json,.md,.html,.css,.xml,.csv,text/*';
        
        input.onchange = (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    resolve({ content: e.target.result, filename: file.name });
                };
                reader.onerror = () => {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: langManager.t('failedToReadFile')
                    });
                    resolve(null);
                };
                reader.readAsText(file);
            } else {
                resolve(null);
            }
        };
        
        input.click();
    });
}

buttonOpen.addEventListener("click", async (e) => {
    console.log("Opening Script");
    
    let result;
    
    if (isFileOpenAccessSupported()) {
        // Use modern File System Access API
        result = await openFileWithPicker();
    } else {
        // Fallback to input method
        result = await openFileAsInput();
    }
    
    if (result && result.content) {
        // Update editor content
        editor_knzl.value = result.content;
        if (editor_var) {
            editor_var.setValue(result.content);
        }
        
        // Clear results when opening new file
        results.innerHTML = "";
        
        // Show success message
        Swal.fire({
            icon: 'success',
            title: langManager.t('scriptLoaded'),
            text: `"${result.filename}" ${langManager.t('loadedSuccessfully')}`,
            timer: 2000,
            showConfirmButton: false
        });
    }
});



// Check if fetch API is supported
function isFetchSupported() {
    return 'fetch' in window;
}

// Function to execute code via AJAX
async function executeCode() {
    const code = editor_knzl.value.trim();
    
    if (!code) {
        Swal.fire({
            icon: 'warning',
            title: langManager.t('emptyScript'),
            text: langManager.t('cannotSaveEmpty')
        });
        return;
    }
    
    // Clear previous results and show loading
    results.innerHTML = "";
    
    // Show inline loader in controls bar
    const loader = document.getElementById('loader');
    const loadingText = document.getElementById('loading-text');
    loadingText.textContent = langManager.t('executing');
    loader.classList.add('show');
    
    // Check if fetch is supported, otherwise fall back to form submission
    if (!isFetchSupported()) {
        console.log('Fetch not supported, falling back to form submission');
        loader.classList.remove('show');
        form.submit(); // This will cause a page reload, but it's the fallback
        return;
    }
    
    try {
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Make AJAX request
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `code=${encodeURIComponent(code)}&csrfmiddlewaretoken=${csrfToken}`
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loader
        loader.classList.remove('show');
        
        // Show results
        const timestamp = new Date().toLocaleTimeString();
        const colors = themeManager.getConsoleColors();
        if (data.output) {
            // Check if there are errors to style them differently
            let outputColor = colors.primary;
            if (data.has_error) {
                outputColor = '#ff6b6b'; // Red color for errors
            }
            results.innerHTML = `<pre style="color: ${outputColor};">[${timestamp}] ${langManager.t('executionCompleted')}\n${data.output}</pre>`;
        } else {
            results.innerHTML = `<pre style="color: ${colors.primary};">[${timestamp}] ${langManager.t('executionCompleted')}\n${langManager.t('noOutput')}</pre>`;
        }
        
        // Auto-scroll to bottom
        setTimeout(scrollToBottom, 100);
        
    } catch (error) {
        console.error('Error executing code:', error);
        loader.classList.remove('show');
        
        results.innerHTML = `<pre style="color: #ff6b6b;">${langManager.t('executionError')}: ${error.message}\n${langManager.t('checkConsole')}</pre>`;
        setTimeout(scrollToBottom, 100);
    }
}

form.addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form submission
    executeCode(); // Execute via AJAX instead
});

buttonClear.addEventListener('click', function() {
  // Clear with console-like feedback
  const grayColor = themeManager.currentTheme === 'light' ? '#6c757d' : '#6c757d';
  results.innerHTML = `<pre style="color: ${grayColor};">${langManager.t('outputCleared')}\n</pre>`;
  
  // Auto-scroll to bottom
  setTimeout(scrollToBottom, 100);
  
  setTimeout(() => {
    results.innerHTML = "";
  }, 1000);
});

buttonClean.addEventListener('click', function() {
    
  Swal.fire({
    title: langManager.t('cleanEditor'),
    showCancelButton: true,
    confirmButtonText: langManager.t('accept'),
    cancelButtonText: langManager.t('cancel'),
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      editor_knzl.value = "";
      editor_var.setValue("");
    }
  })
  }); 

// Save to Local Storage Button
buttonSaveLocal.addEventListener("click", (e) => {
  console.log("Saving script to local storage")
  Swal.fire({
    title: langManager.t('saveStorage'),
    input: 'text',
    inputLabel: langManager.t('scriptName'),
    inputPlaceholder: langManager.t('enterScriptName'),
    inputAttributes: {
      autocapitalize: 'off'
    },
    showCancelButton: true,
    confirmButtonText: langManager.t('saveFile').split(' ')[0], // Just "Save"
    cancelButtonText: langManager.t('cancel'),
    allowOutsideClick: () => !Swal.isLoading(),
    inputValidator: (value) => {
      if (!value) {
        return langManager.t('enterScriptName').replace('...', '!')
      }
    }
  }).then((result) => {
    if (result.isConfirmed) {
      const name = result.value.trim();
      const content = editor_knzl.value;
      
      if (content.trim() === '') {
        Swal.fire({
          icon: 'warning',
          title: langManager.t('emptyScript'),
          text: langManager.t('cannotSaveEmpty')
        });
        return;
      }
      
      const script = scriptStorage.saveScript(name, content);
      renderScriptTree();
      
      Swal.fire({
        icon: 'success',
        title: langManager.t('scriptSaved'),
        text: `"${name}" ${langManager.t('savedToStorage')}`,
        timer: 2000,
        showConfirmButton: false
      });
    }
  })
});

// Refresh Scripts Button
buttonRefreshScripts.addEventListener("click", (e) => {
  renderScriptTree();
  
  Swal.fire({
    icon: 'success',
    title: langManager.t('scriptsRefreshed'),
    timer: 1000,
    showConfirmButton: false
  });
});

// Clear All Scripts Button
buttonClearStorage.addEventListener("click", (e) => {
  const scripts = scriptStorage.getAllScripts();
  
  if (scripts.length === 0) {
    Swal.fire({
      icon: 'info',
      title: langManager.t('noScripts').replace('No scripts stored yet.', 'No Scripts'),
      text: langManager.t('noScripts')
    });
    return;
  }
  
  Swal.fire({
    title: langManager.t('clearAllScripts'),
    text: `${langManager.t('deleteAllScripts')} ${scripts.length} ${langManager.t('savedScripts')}`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: langManager.t('yesClearAll'),
    cancelButtonText: langManager.t('cancel')
  }).then((result) => {
    if (result.isConfirmed) {
      scriptStorage.clearAllScripts();
      renderScriptTree();
      
      Swal.fire({
        icon: 'success',
        title: langManager.t('cleared'),
        text: langManager.t('allScriptsDeleted'),
        timer: 2000,
        showConfirmButton: false
      });
    }
  });
});

// Search functionality
scriptSearch.addEventListener('input', (e) => {
    const searchTerm = e.target.value.trim();
    renderScriptTree(searchTerm);
});

// Enhanced console output formatting
function formatConsoleOutput(output) {
    if (!output) return '';
    
    // Add timestamp and format as console
    const timestamp = new Date().toLocaleTimeString();
    const formattedOutput = output
        .replace(/Error:/g, '<span style="color: #ff6b6b;">Error:</span>')
        .replace(/Warning:/g, '<span style="color: #ffa726;">Warning:</span>')
        .replace(/Success:/g, '<span style="color: #4caf50;">Success:</span>')
        .replace(/True/g, '<span style="color: #4caf50;">True</span>')
        .replace(/False/g, '<span style="color: #ff6b6b;">False</span>')
        .replace(/None/g, '<span style="color: #9e9e9e;">None</span>');
    
    return `[${timestamp}] ${langManager.t('executionCompleted')}\n${formattedOutput}\n`;
}


// Add visual feedback for button clicks
function addButtonFeedback() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });
}

// Enhanced initialization complete




