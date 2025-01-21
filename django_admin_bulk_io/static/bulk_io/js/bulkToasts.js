let timer1, timer2;
let toast, closeIcon, progress

const addElemClass = (elem, class_name) => {
    /**Add Class to Element */
    elem.classList.add(class_name);
};
const removeElemClass = (elem, class_name) => {
    /**Remove Class from Element */
    elem.classList.remove(class_name);

}

const triggerToast = (toastHeader, toastBody) => {
    $(".toast-header").html(toastHeader)
    $(".toast-body").html(toastBody)
    toast.classList.add("active");
    progress.classList.add("active");

    timer1 = setTimeout(() => {
        toast.classList.remove("active");
    }, 5000);

    timer2 = setTimeout(() => {
        progress.classList.remove("active");
    }, 5300);
}

$(document).ready(() => {
    toast = document.querySelector(".toast");
    closeIcon = document.querySelector(".close-toast")
    progress = document.querySelector(".progress");

    closeIcon.addEventListener("click", () => {
        toast.classList.remove("active");
        setTimeout(() => {
            progress.classList.remove("active");
        }, 300);
        clearTimeout(timer1);
        clearTimeout(timer2);
    });
})




// button.addEventListener("click", () => {
//     toast.classList.add("active");
//     progress.classList.add("active");

//     timer1 = setTimeout(() => {
//         toast.classList.remove("active");
//     }, 5000); //1s = 1000 milliseconds

//     timer2 = setTimeout(() => {
//         progress.classList.remove("active");
//     }, 5300);
// });
