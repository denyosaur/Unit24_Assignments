const api_url = "http://127.0.0.1:5000/api"

$(document).ready(async function () {
    console.log("help")
    const resp = await axios.get(`${api_url}/cupcakes`);
    let data = resp.data.cupcakes;
    cupcake_li(data)
})

function cupcake_li(data) {
    cupcakes_list = ""
    for (let cupcake of data) {
        cupcake_info = make_li(cupcake)
        $("#all-cupcakes").append(cupcake_info);
    }
}

function make_li(data) {
    return `
    <li class=${data.id}>
        <ul>
            <li>Flavor:${data.flavor}</li>
            <li>Flavor:${data.size}</li>
            <li>Flavor:${data.rating}</li>
            <li><img src="${data.image}"></li>
        </ul>
    </li>`
}

$("#submit-cupcake").on("click", async function (evt) {
    evt.preventDefault();
    flavor = $("#new-flavor").val();
    size = $("#new-size").val();
    rating = $("#new-rating").val();
    image = $("#new-image").val();
    const new_cupcake = await axios.post(`${api_url}/cupcakes`, { flavor, rating, size, image });
    let data = new_cupcake.data.cupcake;
    $("#all-cupcakes").append(make_li(data))
    $('#new-form').trigger("reset");
})

