<script>
  let restaurants = undefined;
  function getRestaurants(event) {
    // Get the postcode from the input
    let postcode = event.target.postcode.value;
    // Fetch the restaurant data
    fetch("./getRestaurants/" + postcode)
      .then(response => response.json())
      // Set restaurants equal to the response.restaurants data
      .then(response => (restaurants = response.restaurants));
  }

  function getCSV() {
    // Define the CSV rows
    const rows = restaurants;

    // Define the start of the CSV content
    let csvContent = `data:text/csv;charset=utf-8;\n,"Name","Address"\n`;

    // Add the row data to the CSV content
    csvContent += rows.map(row => `"${row.join(`","`)}"`).join("\n");

    // Encode the CSV condent into a URI
    let encodedURI = encodeURI(csvContent);

    // Open up the URI (display a download prompt)
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
