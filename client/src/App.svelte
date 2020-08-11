<script>
  let restaurants = undefined;
  function getRestaurants(event) {
    let postcode = event.target.postcode.value;
    console.log(postcode);
    fetch("./getRestaurants/" + postcode)
      .then(response => response.json())
      .then(response => (restaurants = response.restaurants));
  }

  function getCSV() {
    console.log(restaurants.length);
    const rows = restaurants;
    let csvContent = `data:text/csv;charset=utf-8;\n,"Name","Address"\n`;

    csvContent += rows.map(row => `"${row.join(`","`)}"`).join("\n");

    console.log(csvContent);

    let encodedURI = encodeURI(csvContent);
    window.open(encodedURI);
  }
</script>

<form on:submit|preventDefault={getRestaurants}>
  <label for="postcode">Postcode:</label>
  <input type="text" id="postcode" required />
  <button>Get restaurants</button>
</form>

{#if restaurants}
  <button on:click={getCSV}>Download CSV file</button>

  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Address</th>
      </tr>
    </thead>
    <tbody>
      {#each restaurants as restaurant}
        <tr>
          <td>{restaurant[0]}</td>
          <td>{restaurant[1]}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}
