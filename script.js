

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleMobileMenu);
    }
});

function toggleMobileMenu() {
    const nav = document.querySelector('nav');
    if (nav) {
        nav.classList.toggle('active');
    }
}


function handleLogin(event) {
    event.preventDefault();

    const userType = document.getElementById("userType").value;
    const username = document.getElementById("username").value;

    console.log("User logging in as:", userType);


    sessionStorage.setItem("currentUser", username);
    sessionStorage.setItem("userRole", userType);

    sessionStorage.setItem("userRole", userType);
    if (userType === "influencer") {
        window.location.href = "influencer_dashboard.html";
    } else if (userType === "brand") {
        window.location.href = "brand_dashboard.html";
    } else {
        alert("Please select a valid user type!");
    }
}


function loadDashboard() {
    const user = sessionStorage.getItem("currentUser");


    if (!user) {
        window.location.href = "login.html";
        return;
    }


    const welcomeMsgElement = document.getElementById("welcome-msg");
    if (welcomeMsgElement) {
        welcomeMsgElement.innerText = "👋 Welcome back, " + user + "!";
    }
}

function enableEditMode() {

    document.getElementById('profile-view').style.display = 'none';
    document.getElementById('profile-edit').style.display = 'block';
}

function cancelEditMode() {

    document.getElementById('profile-edit').style.display = 'none';
    document.getElementById('profile-view').style.display = 'block';
}

function saveProfile(event) {
    event.preventDefault();


    const newName = document.getElementById('edit_name').value;
    const newHandle = document.getElementById('edit_handle').value;
    const newIndustry = document.getElementById('edit_industry').value;
    const newField = document.getElementById('edit_field').value;
    const newAge = document.getElementById('edit_age').value;
    const newGender = document.getElementById('edit_gender').value;
    const newLocation = document.getElementById('edit_location').value;
    const newBio = document.getElementById('edit_bio').value;


    document.getElementById('disp_name').innerText = newName;
    document.getElementById('disp_handle').innerText = newHandle;
    document.getElementById('disp_industry').innerText = newIndustry;
    document.getElementById('disp_field').innerText = newField;
    document.getElementById('disp_age').innerText = newAge;
    document.getElementById('disp_gender').innerText = newGender;
    document.getElementById('disp_location').innerText = newLocation;
    document.getElementById('disp_bio').innerText = newBio;


    cancelEditMode();

    alert("Profile Updated Successfully!");
}


function enableEditMode() {
    document.getElementById('profile-view').style.display = 'none';
    document.getElementById('profile-edit').style.display = 'block';
}

function cancelEditMode() {
    document.getElementById('profile-edit').style.display = 'none';
    document.getElementById('profile-view').style.display = 'block';
}

function saveProfile(event) {
    event.preventDefault();


    const newName = document.getElementById('edit_name').value;
    const newHandle = document.getElementById('edit_handle').value;
    const newIndustry = document.getElementById('edit_industry').value;
    const newField = document.getElementById('edit_field').value;
    const newAge = document.getElementById('edit_age').value;
    const newGender = document.getElementById('edit_gender').value;
    const newLocation = document.getElementById('edit_location').value;
    const newBio = document.getElementById('edit_bio').value;


    document.getElementById('disp_name').innerText = newName;
    document.getElementById('disp_handle').innerText = newHandle;
    document.getElementById('disp_industry').innerText = newIndustry;
    document.getElementById('disp_field').innerText = newField;
    document.getElementById('disp_age').innerText = newAge;
    document.getElementById('disp_gender').innerText = newGender;
    document.getElementById('disp_location').innerText = newLocation;
    document.getElementById('disp_bio').innerText = newBio;


    const fileInput = document.getElementById('edit_image');


    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();


        reader.onload = function (e) {

            document.getElementById('disp_image').src = e.target.result;
        }


        reader.readAsDataURL(fileInput.files[0]);
    }


    cancelEditMode();

    alert("Profile Updated Successfully!");
}



function enableEditMode() {
    document.getElementById('profile-view').style.display = 'none';
    document.getElementById('profile-edit').style.display = 'block';
}

function cancelEditMode() {
    document.getElementById('profile-edit').style.display = 'none';
    document.getElementById('profile-view').style.display = 'block';
}

function saveProfile(event) {
    event.preventDefault();


    const newName = document.getElementById('edit_name').value;
    const newHandle = document.getElementById('edit_handle').value;
    const newIndustry = document.getElementById('edit_industry').value;
    const newField = document.getElementById('edit_field').value;
    const newAge = document.getElementById('edit_age').value;
    const newGender = document.getElementById('edit_gender').value;
    const newLocation = document.getElementById('edit_location').value;
    const newBio = document.getElementById('edit_bio').value;


    const newInsta = document.getElementById('edit_insta').value;
    const newTikTok = document.getElementById('edit_tiktok').value;


    document.getElementById('disp_name').innerText = newName;
    document.getElementById('disp_handle').innerText = newHandle;
    document.getElementById('disp_industry').innerText = newIndustry;
    document.getElementById('disp_field').innerText = newField;
    document.getElementById('disp_age').innerText = newAge;
    document.getElementById('disp_gender').innerText = newGender;
    document.getElementById('disp_location').innerText = newLocation;
    document.getElementById('disp_bio').innerText = newBio;


    document.getElementById('disp_insta').innerText = parseInt(newInsta).toLocaleString();
    document.getElementById('disp_tiktok').innerText = parseInt(newTikTok).toLocaleString();


    const fileInput = document.getElementById('edit_image');
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('disp_image').src = e.target.result;
        }
        reader.readAsDataURL(fileInput.files[0]);
    }


    cancelEditMode();

    alert("Profile Updated Successfully!");
}



function filterCampaigns() {

    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const selectedIndustry = document.getElementById('industryFilter').value;


    const cards = document.querySelectorAll('.campaign-card');


    cards.forEach(card => {

        const brand = card.getAttribute('data-brand').toLowerCase();
        const industry = card.getAttribute('data-industry');
        const textContent = card.innerText.toLowerCase();


        const matchesSearch = textContent.includes(searchInput);


        const matchesIndustry = selectedIndustry === "" || industry.includes(selectedIndustry);


        if (matchesSearch && matchesIndustry) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}



function loadBrandDashboard() {
    loadDashboard();


    console.log("Brand Dashboard Loaded");
}

function handleCreateCampaign(event) {
    event.preventDefault();

    const title = document.getElementById('camp_title').value;
    const budget = document.getElementById('camp_budget').value;
    const industry = document.getElementById('camp_industry').value;
    const startDate = document.getElementById('camp_start').value;
    const endDate = document.getElementById('camp_end').value;

    console.log("Creating Campaign:", { title, budget, industry, startDate, endDate });

    alert("Campaign '" + title + "' Created Successfully!");


    window.location.href = "manage_campaigns.html";
}



function enableBrandEdit() {
    document.getElementById('brand-view').style.display = 'none';
    document.getElementById('brand-edit').style.display = 'block';
}

function cancelBrandEdit() {
    document.getElementById('brand-edit').style.display = 'none';
    document.getElementById('brand-view').style.display = 'block';
}

function saveBrandProfile(event) {
    event.preventDefault();


    const name = document.getElementById('edit_brand_name').value;
    const rep = document.getElementById('edit_rep_name').value;
    const email = document.getElementById('edit_brand_email').value;
    const budget = document.getElementById('edit_brand_budget').value;
    const loc = document.getElementById('edit_brand_location').value;
    const bio = document.getElementById('edit_brand_bio').value;
    const industry = document.getElementById('edit_brand_industry').value;


    document.getElementById('disp_brand_name').innerText = name;
    document.getElementById('disp_rep_name').innerText = "Rep: " + rep;
    document.getElementById('disp_brand_email').innerText = email;
    document.getElementById('disp_brand_budget').innerText = "GHS " + parseInt(budget).toLocaleString();
    document.getElementById('disp_brand_location').innerText = loc;
    document.getElementById('disp_brand_bio').innerText = bio;
    document.getElementById('disp_brand_industry').innerText = industry;


    const fileInput = document.getElementById('edit_brand_logo');
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('disp_brand_logo').src = e.target.result;
        }
        reader.readAsDataURL(fileInput.files[0]);
    }

    cancelBrandEdit();
    alert("Company Profile Updated!");
}




function viewCampaign(title, status, budget) {
    const modal = document.getElementById('campaignModal');
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalStatus').innerText = status;
    document.getElementById('modalBudget').innerText = budget;


    const statusElem = document.getElementById('modalStatus');
    if (status === 'Active') statusElem.style.color = '#2ecc71';
    else if (status === 'Pending Start') statusElem.style.color = '#f1c40f';
    else statusElem.style.color = '#bdc3c7';

    modal.style.display = "block";
}


function closeModal() {
    document.getElementById('campaignModal').style.display = "none";
}


window.onclick = function (event) {
    const modal = document.getElementById('campaignModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function editCampaign(title) {

    const confirmEdit = confirm("Do you want to edit details for '" + title + "'?");
    if (confirmEdit) {
        window.location.href = "create_campaign.html";
    }
}


function archiveCampaign(rowId) {
    const confirmArchive = confirm("Are you sure you want to archive this campaign?");
    if (confirmArchive) {
        const row = document.getElementById(rowId);
        if (row) {
            row.style.opacity = '0';
            setTimeout(() => {
                row.remove();
            }, 500);
        }
    }
}



function downloadContract() {

    window.print();
}

function handleTermination() {
    const confirmTerm = confirm("WARNING: Requesting termination will alert the influencer. Are you sure you want to proceed?");

    if (confirmTerm) {

        const btn = document.getElementById("btn-terminate");


        btn.innerText = "Termination Pending";
        btn.style.backgroundColor = "#7f8c8d";
        btn.style.cursor = "not-allowed";
        btn.disabled = true;

        alert("Termination request has been submitted for review.");
    }
}





function downloadContract() {
    window.print();
}

function handleTermination() {
    const confirmTerm = confirm("WARNING: Requesting termination will alert the legal team and the influencer. Are you sure you want to proceed?");

    if (confirmTerm) {

        localStorage.setItem("contract_termination_status", "pending");


        updateBrandTerminationUI();

        alert("Termination request has been submitted for review.");
    }
}


function updateBrandTerminationUI() {
    const btn = document.getElementById("btn-terminate");
    if (btn) {
        btn.innerText = "Termination Pending";
        btn.style.backgroundColor = "#7f8c8d";
        btn.style.cursor = "not-allowed";
        btn.disabled = true;
    }
}


function checkContractStatus() {

    loadDashboard();


    const status = localStorage.getItem("contract_termination_status");

    if (status === "pending") {

        updateBrandTerminationUI();


        const banner = document.getElementById("termination-banner");
        if (banner) {
            banner.style.display = "block";
        }
    }
}






function viewCampaign(title, status, budget) {
    const modal = document.getElementById('campaignModal');
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalStatus').innerText = status;
    document.getElementById('modalBudget').innerText = budget;

    const statusElem = document.getElementById('modalStatus');
    if (status === 'Active') statusElem.style.color = '#2ecc71';
    else if (status === 'Pending Start') statusElem.style.color = '#f1c40f';
    else statusElem.style.color = '#bdc3c7';

    modal.style.display = "block";
}

function closeModal() {
    document.getElementById('campaignModal').style.display = "none";
}

window.onclick = function (event) {
    const modal = document.getElementById('campaignModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}




function editCampaign(title, budget, start, end, industry) {
    const confirmEdit = confirm("Edit details for '" + title + "'?");
    if (confirmEdit) {

        localStorage.setItem("edit_mode", "true");
        localStorage.setItem("edit_title", title);
        localStorage.setItem("edit_budget", budget);
        localStorage.setItem("edit_start", start);
        localStorage.setItem("edit_end", end);

        localStorage.setItem("edit_industry", industry || "Entertainment");


        window.location.href = "create_campaign.html";
    }
}


function checkEditMode() {

    loadBrandDashboard();


    if (localStorage.getItem("edit_mode") === "true") {

        document.getElementById("pageTitle").innerText = "Edit Campaign";
        document.getElementById("submitBtn").innerText = "Update Campaign";


        document.getElementById("camp_title").value = localStorage.getItem("edit_title");
        document.getElementById("camp_budget").value = localStorage.getItem("edit_budget");
        document.getElementById("camp_start").value = localStorage.getItem("edit_start");
        document.getElementById("camp_end").value = localStorage.getItem("edit_end");
        document.getElementById("camp_industry").value = localStorage.getItem("edit_industry");
    }
}


function handleCreateCampaign(event) {
    event.preventDefault();

    const title = document.getElementById('camp_title').value;
    const isEdit = localStorage.getItem("edit_mode") === "true";

    if (isEdit) {
        alert("Campaign '" + title + "' Updated Successfully!");

        localStorage.removeItem("edit_mode");
    } else {
        alert("Campaign '" + title + "' Created Successfully!");
    }

    window.location.href = "manage_campaigns.html";
}

function saveProfile(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('edit_image');


    if (fileInput.files[0]) {
        formData.append('profile_image', fileInput.files[0]);
    }




    const btn = event.target.querySelector('button[type="submit"]');
    const originalText = btn.innerText;
    btn.innerText = "Saving...";

    fetch('/api/update_profile', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Profile saved successfully!");


                if (data.new_image) {
                    document.getElementById('disp_image').src = data.new_image;
                }
                cancelEditMode();
            } else {
                alert("Error saving profile: " + data.message);
            }
        })
        .catch(err => {
            console.error(err);
            alert("Server Error");
        })
        .finally(() => {
            btn.innerText = originalText;
        });
}

function enableEditMode() {
    document.getElementById('profile-view').style.display = 'none';
    document.getElementById('profile-edit').style.display = 'block';
}

function cancelEditMode() {
    document.getElementById('profile-edit').style.display = 'none';
    document.getElementById('profile-view').style.display = 'block';
}

function saveProfile(event) {
    event.preventDefault();
    const btn = event.target.querySelector('button[type="submit"]');
    const originalText = btn.innerText;
    btn.innerText = "Saving...";
    const formData = new FormData(event.target);

    fetch('/api/update_profile', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('disp_name').innerText = document.getElementById('edit_name').value;
                document.getElementById('disp_handle').innerText = document.getElementById('edit_handle').value;
                document.getElementById('disp_industry').innerText = document.getElementById('edit_industry').value;

                if (data.new_image) {
                    document.getElementById('disp_image').src = data.new_image;
                }

                cancelEditMode();
                alert("Profile updated successfully!");
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred.");
        })
        .finally(() => {
            btn.innerText = originalText;
        });
}

function enableBrandEdit() {
    document.getElementById('brand-view').style.display = 'none';
    document.getElementById('brand-edit').style.display = 'block';
}

function cancelBrandEdit() {
    document.getElementById('brand-edit').style.display = 'none';
    document.getElementById('brand-view').style.display = 'block';
}

function saveBrandProfile(event) {
    event.preventDefault();
    const btn = event.target.querySelector('button[type="submit"]');
    const originalText = btn.innerText;
    btn.innerText = "Saving...";

    const formData = new FormData(event.target);

    fetch('/api/update_profile', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('disp_brand_name').innerText = document.getElementById('edit_brand_name').value;
                document.getElementById('disp_brand_email').innerText = document.getElementById('edit_brand_email').value;
                document.getElementById('disp_brand_budget').innerText = "GHS " + document.getElementById('edit_brand_budget').value;

                if (data.new_image) {
                    document.getElementById('disp_brand_logo').src = data.new_image;
                }

                cancelBrandEdit();
                alert("Brand profile updated successfully!");
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred.");
        })
        .finally(() => {
            btn.innerText = originalText;
        });
}
