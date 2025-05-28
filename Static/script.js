let currentOutputId = null;  // This will track which output (quiz or assignment) we're editing

// Function to enable editing of the content (used for both assignment and quiz)
function enableEdit() {
    if (!currentOutputId) return;

    const output = document.getElementById(currentOutputId);
    const editButton = document.getElementById("editButton");

    output.setAttribute('contenteditable', 'true');
    output.style.backgroundColor = "#f9f9f9";
    output.style.border = "1px solid #ccc";
    editButton.textContent = "Save";
    editButton.setAttribute('onclick', 'saveEdit()');
}

// Function to save the edited content
function saveEdit() {
    if (!currentOutputId) return;

    const output = document.getElementById(currentOutputId);
    const editButton = document.getElementById("editButton");

    const editedContent = output.innerHTML;
    console.log("Edited Content: ", editedContent);

    output.setAttribute('contenteditable', 'false');
    output.style.backgroundColor = "#fff";
    output.style.border = "none";
    editButton.textContent = "Edit";
    editButton.setAttribute('onclick', 'enableEdit()');
}

// Quiz generation
async function generateQuiz() {
    const topic = document.getElementById("topic")?.value;
    const quiz_type = document.getElementById("quiz_type")?.value;
    const num_questions = document.getElementById("num_questions")?.value;
    const education_level = document.getElementById("education_level")?.value;

    if (!topic || !quiz_type || !num_questions || !education_level) return;

    const outputElement = document.getElementById("quizOutput");
    const loader = document.getElementById("loadingIndicator");

    outputElement.innerHTML = "";
    loader.style.display = "block";

    try {
        const response = await fetch('/generate_quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic,
                quiz_type,
                num_questions,
                education_level
            })
        });

        const data = await response.json();
        loader.style.display = "none";

        let content = data.quiz_content?.trim() || "";
        const lines = content.split('\n');
        if (lines[0].toLowerCase().startsWith("here's a quiz")) {
            lines.shift();
        }
        content = lines.join('\n');

        outputElement.innerHTML = content.replace(/\n/g, "<br>");

        // Update current output and show buttons
        currentOutputId = "quizOutput";
        document.getElementById("editButton").style.display = "inline-block";
        const downloadLink = document.getElementById("downloadLink");
        downloadLink.style.display = "inline-block";
        downloadLink.href = "/download_quiz";

    } catch (error) {
        loader.style.display = "none";
        outputElement.innerHTML = "<p style='color: red;'>Failed to generate quiz. Please try again later.</p>";
    }
}

// Assignment generation
async function generateAssignment() {
    const topic = document.getElementById("topic").value;
    const assignment_type = document.getElementById("assignment_type").value;
    const num_questions = document.getElementById("num_questions").value;
    const education_level = document.getElementById("education_level").value;

    if (!topic || !assignment_type || !num_questions || !education_level) {
        alert("Please fill in all fields.");
        return;
    }

    const outputElement = document.getElementById("assignmentOutput");
    const loader = document.getElementById("loadingIndicator");

    outputElement.innerHTML = "";
    loader.style.display = "block";

    try {
        const response = await fetch('/generate_assignment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic,
                assignment_type,
                num_questions,
                education_level
            })
        });

        const data = await response.json();
        loader.style.display = "none";

        if (data.error) {
            outputElement.innerHTML = `<p style='color: red;'>${data.error}</p>`;
            return;
        }

        let content = data.assignment_content?.trim() || "";
        const lines = content.split('\n');
        if (lines[0].toLowerCase().startsWith("here's an assignment")) {
            lines.shift();
        }
        content = lines.join('\n');

        outputElement.innerHTML = content.replace(/\n/g, "<br>");

        // Update current output and show buttons
        currentOutputId = "assignmentOutput";
        document.getElementById("editButton").style.display = "inline-block";
        const downloadLink = document.getElementById("downloadLink");
        downloadLink.style.display = "inline-block";
        downloadLink.href = "/download_assignment";

    } catch (error) {
        loader.style.display = "none";
        outputElement.innerHTML = "<p style='color: red;'>Failed to generate assignment. Please try again later.</p>";
    }
}


async function generateCourseOutline() {
    const courseData = {
        course_title: document.getElementById('course_title').value,
        course_code: document.getElementById('course_code').value,
        education_level: document.getElementById('education_level').value,
        credit_hours: document.getElementById('credit_hours').value,
        prerequisites: document.getElementById('prerequisites').value
    };

    // Show loading and clear previous output
    const outputElement = document.getElementById('courseOutlineOutput');
    outputElement.innerHTML = "Generating course outline... Please wait.";
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('generateButton').disabled = true;

    try {
        const response = await fetch('/generate_course_outline', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(courseData)
        });

        const data = await response.json();

        document.getElementById('loadingIndicator').style.display = 'none';
        document.getElementById('generateButton').disabled = false;

        if (data.error) {
            alert("Error: " + data.error);
            outputElement.innerHTML = "";
            return;
        }

        // Show generated content with line breaks
        outputElement.innerHTML = data.course_outline.replace(/\n/g, "<br>");
        currentOutputId = "courseOutlineOutput";  // Set current editable output id

        // Show edit and download buttons
        document.getElementById('editButton').style.display = 'inline-block';
        const downloadLink = document.getElementById('downloadLink');
        downloadLink.href = '/download_co';
        downloadLink.style.display = 'inline-block';

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loadingIndicator').style.display = 'none';
        document.getElementById('generateButton').disabled = false;
        alert('Something went wrong. Please try again.');
        outputElement.innerHTML = "";
    }
}


// Grading & Feedback generation
async function generateGradingFeedback() {
    const subject = document.getElementById("gf_subject")?.value;
    const education_level = document.getElementById("gf_education_level")?.value;
    const mark_out_of = document.getElementById("gf_mark_out_of")?.value;
    const fileInput = document.getElementById("gf_file_upload");
    const pastedText = document.getElementById("gf_pasted_text")?.value;

    if (!subject || !education_level || !mark_out_of) {
        alert("Please fill in Subject, Education Level, and Mark Out Of.");
        return;
    }

    const outputElement = document.getElementById("gfOutput");
    const loader = document.getElementById("gf_loadingIndicator");

    outputElement.innerHTML = "";
    loader.style.display = "block";

    let fileContent = "";

    if (fileInput.files.length > 0) {
        // Read the file content as text (simple approach; for .docx/.pdf you'd need extra parsing on backend)
        const file = fileInput.files[0];
        fileContent = await file.text();
    }

    // Prefer pasted text if available, else file content
    const submissionText = pastedText.trim() || fileContent.trim();

    if (!submissionText) {
        alert("Please either upload a file or paste the student's submission text.");
        loader.style.display = "none";
        return;
    }

    try {
        const response = await fetch('/generate_feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                subject,
                education_level,
                mark_out_of,
                submission_text: submissionText
            })
        });

        const data = await response.json();
        loader.style.display = "none";

        if (data.error) {
            outputElement.innerHTML = `<p style='color: red;'>${data.error}</p>`;
            return;
        }

        let content = data.feedback_content?.trim() || "";

        // Remove any leading explanations (optional)
        const lines = content.split('\n');
        if (lines[0].toLowerCase().startsWith("here's grading")) {
            lines.shift();
        }
        content = lines.join('\n');

        outputElement.innerHTML = content.replace(/\n/g, "<br>");

        // Update current output and show buttons
        currentOutputId = "gfOutput";
        document.getElementById("gf_editButton").style.display = "inline-block";

        const downloadLink = document.getElementById("gf_downloadLink");
        downloadLink.style.display = "inline-block";
        downloadLink.href = "/download_grading_feedback";  // You should create this route if you want download support

    } catch (error) {
        loader.style.display = "none";
        outputElement.innerHTML = "<p style='color: red;'>Failed to generate grading and feedback. Please try again later.</p>";
    }
}
