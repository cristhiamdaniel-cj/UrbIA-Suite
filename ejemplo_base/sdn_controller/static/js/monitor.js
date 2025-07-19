async function cargarDatos() {
  const portRes = await fetch("/stats/ports");
  const flowRes = await fetch("/stats/flows");

  const ports = await portRes.json();
  const flows = await flowRes.json();

  // === GRÁFICA DE PUERTOS ===
  const sids = Object.keys(ports);
  const s1_ports = ports[sids[0]];
  const labels = s1_ports.map(p => "Puerto " + p.puerto);
  const rx = s1_ports.map(p => p.rx_bytes);
  const tx = s1_ports.map(p => p.tx_bytes);

  const ctx = document.getElementById("puertosChart").getContext("2d");
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        { label: 'RX Bytes', data: rx, backgroundColor: 'blue' },
        { label: 'TX Bytes', data: tx, backgroundColor: 'green' }
      ]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });

  // === TABLA DE FLUJOS ===
  const contenedor = document.getElementById("tabla-flujos");
  contenedor.innerHTML = '';

  for (const [dpid, reglas] of Object.entries(flows)) {
    const title = document.createElement("h5");
    title.textContent = `Switch ${dpid}`;
    contenedor.appendChild(title);

    const table = document.createElement("table");
    table.className = "table table-bordered table-sm table-striped";

    const thead = document.createElement("thead");
    thead.innerHTML = `
      <tr class="table-light">
        <th>Prioridad</th><th>In Port</th><th>Tipo</th><th>IPv4 Src</th><th>IPv4 Dst</th><th>Paquetes</th><th>Bytes</th>
      </tr>
    `;
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    reglas.forEach(flujo => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${flujo.prioridad}</td>
        <td>${flujo.in_port ?? '-'}</td>
        <td>${flujo.eth_type == 2048 ? 'IPv4' : '-'}</td>
        <td>${flujo.ipv4_src ?? '-'}</td>
        <td>${flujo.ipv4_dst ?? '-'}</td>
        <td>${flujo.paquetes}</td>
        <td>${flujo.bytes}</td>
      `;
      tbody.appendChild(fila);
    });

    table.appendChild(tbody);
    contenedor.appendChild(table);
  }
}
cargarDatos();
