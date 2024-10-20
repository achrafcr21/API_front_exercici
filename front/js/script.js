document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch('http://127.0.0.1:8000/alumne/list')
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");
                // Nombre del Alumno
                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.NomAlumne;
                row.appendChild(nomAluCell);

                // Repetir per tots els altres camps restants que retorna l'endpoint
 
                 // Ciclo del Alumno
                 const cicloCell = document.createElement("td");
                 cicloCell.textContent = alumne.Cicle;
                 row.appendChild(cicloCell);
 
                 // Curs del Alumno
                 const cursCell = document.createElement("td");
                 cursCell.textContent = alumne.Curs; 
                 row.appendChild(cursCell);
 
                 // Grupo del Alumno
                 const grupoCell = document.createElement("td");
                 grupoCell.textContent = alumne.Grup;
                 row.appendChild(grupoCell);
 
                 // Descripción del Aula
                 const descAulaCell = document.createElement("td");
                 descAulaCell.textContent = alumne.DescAula; // Este es el campo donde se muestra la descripción del aula
                 row.appendChild(descAulaCell);

                

                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});