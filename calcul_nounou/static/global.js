const urlToFlask = "http://127.0.0.1:5000/";

/////////////////////////////////////////// Register js ///////////////////////////////////////////

const sendNewDay = async (formdata, form) => {

    let r = await fetch(urlToFlask+'data_csv/newDay', 
    {
        method: "POST", 
        body: formdata, 
        headers:{
            "Accept":"application/json"
        }
    });
    
    if(r.ok === true){
        let data = await r.json();

        if(data.status == 200){
            form.reset();
            Swal.fire({
                position: 'top-end',
                icon: 'success',
                title: 'Journée enregistrée.',
                showConfirmButton: false,
                timer: 1000
            })
        }
        else{
            Swal.fire({
                icon: 'error',
                title: data.message,
            })
        }
    }
}


function isFormValid(){
    const form = document.getElementById('formRegisterDay');
    let formdata = new FormData(form);

    let errorMessage = "";

    const date = formdata.get('dateRegister')
    const year = Number(date.split('-')[0]);
    const hourIn = formdata.get('hourIn')
    const onlyHourIn = Number(hourIn.split(':')[0]);
    const hourOut = formdata.get('hourOut')
    const onlyHourOut = Number(hourOut.split(':')[0]);

    if(date == "" || (year < 2023 || year > 2025)){
        errorMessage += "La date n'est pas renseigneé ou n'est pas au bon format.";
    }
    if(onlyHourOut < onlyHourIn || hourIn == "" || hourOut == ""){
        errorMessage += "Les heures ne sont pas correctement renseignées.";
    }
    
    if(errorMessage != ""){
        Swal.fire({
            icon: 'error',
            title: errorMessage,
          })
    }
    else{
        sendNewDay(formdata, form);
    }
}


/////////////////////////////////////////// Details js ///////////////////////////////////////////


/////////////////////// get Data from csv ///////////////////////

Array.from(document.querySelectorAll("#div-year button")).forEach(btn => {
    btn.addEventListener('click', event => changeSelect(btn, "#div-year button.select"));
});

Array.from(document.querySelectorAll("#div-month button")).forEach(btn => {
    btn.addEventListener('click', event => changeSelect(btn, "#div-month button.select"));
});

function changeSelect(btn, selector){
    document.querySelector(selector).classList.remove("select")
    btn.classList.add("select");
}

const showDetails = async () => {
    const year = document.querySelector("#div-year button.select").textContent;
    const month = document.querySelector("#div-month button.select").getAttribute('value');
    let r = await fetch(urlToFlask+'data_csv/detailsMonth/'+year+"-"+month, 
    {
        method: "GET",  
        headers:{
            "Accept":"application/json"
        }
    });
    
    if(r.ok === true){
        let data = await r.json();
        if(data.status==200){
            const monthFix = Number(document.querySelector('#select-month-cost').value);

            document.querySelector("#div-details").innerHTML = data.tab_data;
            document.querySelector("#span-hours").innerText = data.totalHours;
            document.querySelector("#span-cout").innerText = data.totalCostMonth;
            document.querySelector("#span-month-fix").innerText = monthFix;
            document.querySelector("#span-month-total").innerText = (monthFix + data.totalCostMonth).toFixed(2);;
            document.querySelector("#btn-pdf").classList.remove("d-none")
        }
        else{
            document.querySelector("#div-details").innerHTML = "<h2>"+data.message+"</h2>";
            document.querySelector("#btn-pdf").classList.add("d-none")
        }
    }
}

////////////////////////// update csv //////////////////////////

function update(){
    Array.from(document.querySelectorAll("#div-details tbody tr")).forEach(tr => {

        const lstTd = Array.from(tr.querySelectorAll("td"));
        const lstClasses = ["bg-warning", "update"]
        lstTd[2].classList.add(...lstClasses);
        lstTd[3].classList.add(...lstClasses);
        lstTd[2].addEventListener('click', event => updateValue(event.target));
        lstTd[3].addEventListener('click', event => updateValue(event.target));

    });
}

function updateValue(hourElement){
    Swal.fire({
        title: 'Nouvel horaire :',
        html:'<input type="time" id="newHour" value="'+hourElement.innerHTML+'">',
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText:'Enregistrer',
        cancelButtonText:'Annuler',
    }).then((result) => {
        if (result.isConfirmed) {
            hourElement.innerHTML = document.querySelector("#newHour").value
            updateInCsv(hourElement);
        }
    })    
}

const updateInCsv = async (tdUpdate) => {
    const tr = tdUpdate.closest("tr");
    const updateLine = {
        dateRegister: tr.children[2].innerText,
        hourIn: tr.children[3].innerText,
        hourOut: tr.children[4].innerText
    }
    let r = await fetch(urlToFlask+'data_csv/updateLine', 
    {
        method: "POST", 
        body: JSON.stringify(updateLine), 
        headers:{
            "Content-type":"application/json; charset=UTF-8",
            "Accept":"application/json"
        }
    });
    if(r.ok === true){
        showDetails();
    }
}


//////////////////// Delete row ///////////////////////

function deleteRow(){
    Array.from(document.querySelectorAll("#div-details tbody tr")).forEach(tr => {

        const lstTd = Array.from(tr.querySelectorAll("td"));
        const lstClasses = ["bg-danger", "update"]
        lstTd[1].classList.add(...lstClasses);
        lstTd[1].addEventListener('click', event => deleteValue(event.target));

    });
}

function deleteValue(dateElement){
    Swal.fire({
        title: 'Supprimer la journée de '+dateElement.innerHTML+'?',
        showCancelButton: true,
        confirmButtonText: 'Supprimer',
        denyButtonText: `Annuler`,
      }).then((result) => {

        if (result.isConfirmed) {
            deleteInCsv(dateElement);
        } 
    })
}
const deleteInCsv = async (tdDelete) => {
    const tr = tdDelete.closest("tr");
    const deleteLine = {
        dateRegister: tr.children[2].innerText,
    }
    let r = await fetch(urlToFlask+'data_csv/deleteLine', 
    {
        method: "POST", 
        body: JSON.stringify(deleteLine), 
        headers:{
            "Content-type":"application/json; charset=UTF-8",
            "Accept":"application/json"
        }
    });
    if(r.ok === true){
        showDetails();
    }
}


//////////////////// PDF ///////////////////////

function toPdf(){
    const elt = document.querySelector("#div-tab");
    const month = document.querySelector("#div-month button.select").innerText;
    const year = document.querySelector("#div-year button.select").innerText;

    const opt = {
        filename: 'recap-'+month+'-'+year+'.pdf',
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      };

    html2pdf()
    .set(opt)
    .from(elt)
    .save();
}