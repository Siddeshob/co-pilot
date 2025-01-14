// Handle file upload
document.getElementById("uploadForm").onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();
    document.getElementById("uploadResult").textContent = result.message;
    loadFiles(); // Refresh file list
  } catch (error) {
    document.getElementById("uploadResult").textContent =
      "Upload failed: " + error;
  }
};

// Load and display files
async function loadFiles() {
  try {
    const response = await fetch("/files");
    const data = await response.json();
    const fileList = document.getElementById("fileList");
    fileList.innerHTML = data.files.length ? "" : "No files uploaded";
    data.files.forEach((file) => {
      const div = document.createElement("div");
      div.className = "file-link";
      div.textContent = file;
      div.onclick = () => viewFile(file);
      fileList.appendChild(div);
    });
  } catch (error) {
    console.error("Error loading files:", error);
  }
}

async function viewFile(filename) {
    try {
        const response = await fetch(`/file/${filename}`);
        const data = await response.json();
        
        // Get container elements
        const container = document.getElementById('contentContainer');
        const contentView = document.getElementById('pdfContentView');
        const filenameElement = document.getElementById('contentFilename');
        
        // Show the container
        container.classList.remove('hidden');
        
        // Set the filename
        filenameElement.textContent = filename;
        
        // Clear previous content
        contentView.innerHTML = '';

        if (filename.toLowerCase().endsWith('.csv') ) {
            // Format CSV data as table
            const tableHtml = createTableFromData(data.content);
            contentView.innerHTML = tableHtml;
        } else {
            // For other files, format as pretty JSON

            const textContent = data.content.content || data.content;
            contentView.innerHTML = `<div class="text-content">${textContent}</div>`;

            console.log(textContent)
            
        }
        
        // Scroll to the content
        container.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error("Error viewing file:", error);
        alert("Error loading file content");
    }
}

function createTableFromData(data) {
    // Create table headers
    const headers = Object.keys(data);
    let tableHtml = '<table class="data-table"><thead><tr>';
    
    // Add headers
    headers.forEach(header => {
        tableHtml += `<th>${header}</th>`;
    });
    tableHtml += '</tr></thead><tbody>';
    
    // Get the number of rows (length of first column's data)
    const rowCount = data[headers[0]].length;
    
    // Add data rows
    for (let i = 0; i < rowCount; i++) {
        tableHtml += '<tr>';
        headers.forEach(header => {
            tableHtml += `<td>${data[header][i]}</td>`;
        });
        tableHtml += '</tr>';
    }
    
    tableHtml += '</tbody></table>';
    return tableHtml;
}

function closeContent() {
    const container = document.getElementById('contentContainer');
    container.classList.add('hidden');
}




// Load files when page loads
loadFiles();

