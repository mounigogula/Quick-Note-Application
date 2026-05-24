async function fetchNotes() {

    const response = await fetch('/get_notes');

    const notes = await response.json();

    const notesContainer =
    document.getElementById('notesContainer');

    const noteCount =
    document.getElementById('noteCount');

    notesContainer.innerHTML = "";

    noteCount.innerText = notes.length;

    notes.forEach(note => {

        const noteDiv =
        document.createElement('div');

        noteDiv.classList.add('note');

        noteDiv.innerHTML = `
            <small>${note.created_at}</small>

            <p>${note.content}</p>

            <button class="delete-btn"
            onclick="deleteNote(${note.id})">

                Delete

            </button>
        `;

        notesContainer.appendChild(noteDiv);
    });
}

async function saveNote() {

    const noteInput =
    document.getElementById('noteInput');

    const content = noteInput.value;

    await fetch('/add_note', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({content})
    });

    noteInput.value = "";

    fetchNotes();
}

async function deleteNote(id) {

    await fetch(`/delete_note/${id}`, {

        method: 'DELETE'
    });

    fetchNotes();
}

fetchNotes();