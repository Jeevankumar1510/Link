async function shortenURL(){

    const url =
    document.getElementById(
        "urlInput"
    ).value;

    const response =
    await fetch(
        "/api/shorten",
        {
            method:"POST",
            headers:{
                "Content-Type":
                "application/json"
            },
            body:JSON.stringify({
                url:url
            })
        }
    );

    const data =
    await response.json();

    document
    .getElementById(
        "linksContainer"
    )
    .innerHTML += `
    <p>
    ${data.short_url}
    </p>
    `;
}