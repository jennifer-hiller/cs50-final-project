document.querySelectorAll(".like-this").forEach(button => {
    button.addEventListener("click", async () => {
        console.log(button.dataset.action);
        const response = await fetch("/like", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tweet: button.dataset.tweetId,
                action: button.dataset.action,
            })
        });
        const data = await response.json();
        if (data.status === "success") {
            if (button.dataset.action === "like") {
                button.dataset.action = "dislike";
                button.querySelector("img").attributes.getNamedItem("src").value = "/static/heart_filled.svg";
            } else {
                button.dataset.action = "like";
                button.querySelector("img").attributes.getNamedItem("src").value = "/static/heart_empty.svg";
            }
            const tweetLikes = button.closest(".card").querySelector(".tweet-likes");
            tweetLikes.textContent = data.likes;
        } else {
            alert("Error changing tweet status");
        }
    });
});
document.querySelectorAll(".logged-out").forEach(button => {
    button.addEventListener("click", () => {
        alert("You must be logged in to do that");
    });
});