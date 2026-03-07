import React, { useState } from 'react'

type Producto = {
  id: number;
  producto: string;
  categoria: string;
  cantidad: number;
  precio: number;
  subtotal: number;
};

function App() {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [bitacora, setBitacora] = useState<string[]>([]);
  const [jsonGenerado, setJsonGenerado] = useState<string>("");
  const [totalGeneral, setTotalGeneral] = useState<number>(0);

  const agregarBitacora = (mensaje: string): void => {
    setBitacora((prev) => [...prev, mensaje]);
  };

  const leerArchivo = async (event: React.ChangeEvent<HTMLInputElement>): Promise<void> => {
    const archivo = event.target.files?.[0];
    if (!archivo) return;

    setProductos([]);
    setBitacora([]);
    setJsonGenerado("");
    setTotalGeneral(0);

    agregarBitacora(`Archivo seleccionado: ${archivo.name}`);

    const texto = await archivo.text();

    const lineas = texto
      .split("\n")
      .map((linea: string) => linea.trim())
      .filter((linea: string) => linea.length > 0);

    const productosProcesados: Producto[] = [];
    let errores = 0;
    let total = 0;

    lineas.forEach((linea: string, index: number) => {
      const partes = linea.split("|").map((p: string) => p.trim());

      if (partes.length !== 4) {
        errores++;
        agregarBitacora(`Línea ${index + 1} inválida: ${linea}`);
        return;
      }

      const [producto, categoria, cantidadTexto, precioTexto] = partes;

      const cantidad = Number(cantidadTexto);
      const precio = Number(precioTexto);

      if (isNaN(cantidad) || isNaN(precio)) {
        errores++;
        agregarBitacora(
          `Línea ${index + 1} inválida por cantidad o precio no numérico.`
        );
        return;
      }

      const subtotal = cantidad * precio;
      total += subtotal;

      const item: Producto = {
        id: index + 1,
        producto,
        categoria,
        cantidad,
        precio,
        subtotal,
      };

      productosProcesados.push(item);
      agregarBitacora(`Línea ${index + 1} procesada correctamente.`);
    });

    setProductos(productosProcesados);
    setTotalGeneral(total);
    setJsonGenerado(JSON.stringify(productosProcesados, null, 2));

    agregarBitacora(
      `Proceso finalizado. Productos válidos: ${productosProcesados.length}, errores: ${errores}`
    );
  };

  const descargarJSON = (): void => {
    if (!jsonGenerado) return;

    const blob = new Blob([jsonGenerado], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const enlace = document.createElement("a");
    enlace.href = url;
    enlace.download = "dispensa.json";
    enlace.click();

    URL.revokeObjectURL(url);
    agregarBitacora("Archivo JSON descargado.");
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>RPA Frontend - Dispensa de Supermercado</h1>
      <p>
        Este robot lee un archivo TXT de compras, procesa automáticamente los
        productos y genera una tabla con total y JSON.
      </p>

      <input type="file" accept=".txt" onChange={leerArchivo} />

      <hr />

      <h2>Productos procesados</h2>
      {productos.length > 0 ? (
        <table
          border={1}
          cellPadding={8}
          style={{ borderCollapse: "collapse", width: "100%" }}
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Producto</th>
              <th>Categoría</th>
              <th>Cantidad</th>
              <th>Precio</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((item: Producto) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.producto}</td>
                <td>{item.categoria}</td>
                <td>{item.cantidad}</td>
                <td>Q{item.precio.toFixed(2)}</td>
                <td>Q{item.subtotal.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No hay productos cargados.</p>
      )}

      <h2>Total general: Q{totalGeneral.toFixed(2)}</h2>

      <hr />

      <h2>JSON generado</h2>
      <textarea
        value={jsonGenerado}
        readOnly
        rows={18}
        cols={100}
      />

      <br />
      <br />

      <button onClick={descargarJSON} disabled={!jsonGenerado}>
        Descargar JSON
      </button>

      <hr />

      <h2>Bitácora del robot</h2>
      <ul>
        {bitacora.map((mensaje: string, index: number) => (
          <li key={index}>{mensaje}</li>
        ))}
      </ul>
    </div>
  );
}

export default App
