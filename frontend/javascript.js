async function shortenURL() {

    const url =
    document.getElementById("urlInput").value;

    const response =
    await fetch("/api/shorten", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: url
        })
    });

    const data = await response.json();

    const shortUrl =
    window.location.origin +
    data.short_url;

    const container =
    document.getElementById(
        "linksContainer"
    );

    container.innerHTML += `
    <div class="link-card">

        <p>
            <strong>Original URL:</strong>
            ${url}
        </p>

        <p>
            <strong>Short URL:</strong>
            <a href="${shortUrl}" target="_blank">
                ${shortUrl}
            </a>
        </p>

    </div>
    `;
}