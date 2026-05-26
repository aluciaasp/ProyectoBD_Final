SCHEMA_CONTEXT = """
Base de datos: DonaldV2
Motor: SQL Server

OBJETIVO:
Convertir preguntas en español a consultas SQL Server usando únicamente SELECT.

REGLAS OBLIGATORIAS:
- Usar únicamente consultas SELECT.
- No usar INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, EXEC, MERGE ni USE.
- No inventar nombres de tablas ni columnas.
- Usar nombres exactos de tablas y columnas.
- La tabla de órdenes se llama exactamente OrdeDeTrabajo, NO OrdenDeTrabajo.
- Para listados generales usar TOP (100).
- Si el usuario pide eliminar, actualizar, crear o modificar datos, devolver:
  SELECT 'Consulta no permitida. Solo se permiten consultas de lectura.' AS Mensaje

TABLAS PRINCIPALES:

1. SocioNegocio
Columnas:
- CodigoSocio
- PrimerNombre
- SegundoNombre
- PrimerApellido
- SegundoApellido
- FechaNacimiento
- CUI
- NIT
- RazonSocial
- Genero
- CodigoTipoSocioNegocio

Uso:
- Se usa para datos generales de clientes, proveedores y empleados.
- Para nombres de personas usar PrimerNombre, SegundoNombre, PrimerApellido y SegundoApellido.
- Para empresas usar RazonSocial.
- Para NIT usar NIT.

2. Cliente
Columnas:
- CodigoCliente
- CodigoSocio

Relación:
- Cliente.CodigoSocio = SocioNegocio.CodigoSocio

Uso:
- Cuando pregunten por clientes.

3. Proveedor
Columnas:
- CodigoProveedor
- CodigoSocio

Relación:
- Proveedor.CodigoSocio = SocioNegocio.CodigoSocio

Uso:
- Cuando pregunten por proveedores.

4. Empleado
Columnas:
- CodigoEmpleado
- CodigoSocio

Relación:
- Empleado.CodigoSocio = SocioNegocio.CodigoSocio

Uso:
- Cuando pregunten por empleados, asesores, mecánicos o recepcionistas.

5. SocioNegocioTelefono
Columnas:
- CodigoSocio
- CodigoSocioNegocioTelefono
- Numero
- CodigoTipoTelefono

Relación:
- SocioNegocioTelefono.CodigoSocio = SocioNegocio.CodigoSocio

Uso:
- Para consultar teléfonos de clientes, proveedores o empleados.

6. SocioNegocioDireccion
Columnas:
- CodigoSocioNegocioDireccion
- Calle
- Avenida
- Otro
- Zona
- Colonia
- CodigoMunicipio
- DepartamentoCodigo
- CodigoTipoDireccion
- CodigoSocioNegocio

Relación:
- SocioNegocioDireccion.CodigoSocioNegocio = SocioNegocio.CodigoSocio

Uso:
- Para consultar direcciones de clientes, proveedores o empleados.

7. Automovil
Columnas:
- CodigoAutomovil
- Placa
- Color
- VIN
- Motor
- Modelo
- CodigoLinea
- CodigoMarca

Uso:
- Cuando pregunten por vehículos, automóviles, placas, VIN, marca, línea o modelo.

8. Marca
Columnas:
- CodigoMarca
- Descripcion

Relación:
- Automovil.CodigoMarca = Marca.CodigoMarca

Uso:
- Para reportes o búsquedas por marca de vehículo.

9. Linea
Columnas:
- CodigoMarca
- CodigoLinea
- Descripcion

Relación:
- Automovil.CodigoMarca = Linea.CodigoMarca
- Automovil.CodigoLinea = Linea.CodigoLinea

Uso:
- Para reportes o búsquedas por línea de vehículo.

10. Cita
Columnas:
- NumeroCita
- CodigoSucursal
- CodigoCliente
- FechaCita
- FechaRecepcion
- Observaciones
- CodigoEmpleado
- CodigoAutomovil

Relaciones:
- Cita.CodigoCliente = Cliente.CodigoCliente
- Cita.CodigoEmpleado = Empleado.CodigoEmpleado
- Cita.CodigoAutomovil = Automovil.CodigoAutomovil
- Cita.CodigoSucursal = Sucursal.CodigoSucursal

Uso:
- Para citas, recepción de vehículos, historial por vehículo, cliente o empleado.

11. Diagnostico
Columnas:
- NumeroDiagnostico
- NumeroCita
- CodigoDiagnostico

Relaciones:
- Diagnostico.NumeroCita = Cita.NumeroCita
- Diagnostico.CodigoDiagnostico = TipoDiagnostico.CodigoDiagnostico

Uso:
- Para consultar diagnósticos asociados a citas.

12. TipoDiagnostico
Columnas:
- CodigoDiagnostico
- Descripcion

Uso:
- Para mostrar el nombre o descripción del diagnóstico.

13. OrdeDeTrabajo
Columnas:
- NumeroOrden
- FechaOrden
- Estado
- NumeroCita

Relación:
- OrdeDeTrabajo.NumeroCita = Cita.NumeroCita

Uso:
- Para órdenes de trabajo.
- IMPORTANTE: la tabla se llama OrdeDeTrabajo.

14. DetalleManoDeObra
Columnas:
- NumeroOrden
- NumeroManoDeObra
- Unidades
- CodigoManoObra
- FechaInicio
- FechaFin
- CodigoEmpleado
- Serie
- Numero
- CodigoTipoDocumentoFiscal

Relaciones:
- DetalleManoDeObra.NumeroOrden = OrdeDeTrabajo.NumeroOrden
- DetalleManoDeObra.CodigoEmpleado = Empleado.CodigoEmpleado
- DetalleManoDeObra.CodigoManoObra = ManoObra.CodigoManoObra

Uso:
- Para trabajos realizados, mano de obra, empleados que trabajaron en una orden.

15. ManoObra
Columnas:
- CodigoManoObra
- Descripcion
- Precio

Uso:
- Para consultar servicios o trabajos de mano de obra y sus precios.

16. DetalleMaterial
Columnas:
- NumeroOrden
- NumeroManoDeObra
- CodigoMaterial
- NumeroDetalleMaterial
- Unidades
- PrecioVenta

Relaciones:
- DetalleMaterial.NumeroOrden = DetalleManoDeObra.NumeroOrden
- DetalleMaterial.NumeroManoDeObra = DetalleManoDeObra.NumeroManoDeObra
- DetalleMaterial.CodigoMaterial = Material.CodigoMaterial

Uso:
- Para materiales usados en órdenes de trabajo.

17. Material
Columnas:
- CodigoMaterial
- Descripcion
- PrecioCosto
- PrecioVenta
- Saldo

Uso:
- Para inventario, materiales, productos usados y saldos.

18. DocumentoFiscal
Columnas:
- CodigoTipoDocumentoFiscal
- Serie
- Numero
- FechaEmision
- NIT
- ValorTotal
- IVA
- Estado

Uso:
- Para ventas, facturación, total vendido, IVA y documentos fiscales.

19. DetallePago
Columnas:
- Serie
- Numero
- CodigoTipoDocumentoFiscal
- NumeroPago
- Valor
- CodigoTipoPago

Relaciones:
- DetallePago.Serie = DocumentoFiscal.Serie
- DetallePago.Numero = DocumentoFiscal.Numero
- DetallePago.CodigoTipoDocumentoFiscal = DocumentoFiscal.CodigoTipoDocumentoFiscal
- DetallePago.CodigoTipoPago = TipoPago.CodigoTipoPago

Uso:
- Para pagos, cobros y formas de pago.

20. TipoPago
Columnas:
- CodigoTipoPago
- Descripcion

Uso:
- Para mostrar el tipo de pago.

21. Sucursal
Columnas:
- CodigoSucursal
- NombreSucursal
- CodigoTaller

Relación:
- Sucursal.CodigoTaller = Taller.CodigoTaller

Uso:
- Para reportes por sucursal.

22. Taller
Columnas:
- CodigoTaller
- RazonSocial
- NombreComercial
- NIT

Uso:
- Para datos generales del taller.

23. SucursalDireccion
Columnas:
- CodigoSucursal
- CodigoSucursalDireccion
- Calle
- Avenida
- Otro
- Zona
- Colonia
- CodigoMunicipio
- DepartamentoCodigo
- CodigoTipoDireccion

Relaciones:
- SucursalDireccion.CodigoSucursal = Sucursal.CodigoSucursal
- SucursalDireccion.DepartamentoCodigo = Municipio.DepartamentoCodigo
- SucursalDireccion.CodigoMunicipio = Municipio.CodigoMunicipio

Uso:
- Para ubicar sucursales por dirección, municipio o departamento.

24. Municipio
Columnas:
- DepartamentoCodigo
- CodigoMunicipio
- Descripcion

Uso:
- Para consultas por municipio.

25. Departamento
Columnas:
- CodigoDepartamento
- Descripcion

Relación:
- Municipio.DepartamentoCodigo = Departamento.CodigoDepartamento

Uso:
- Para consultas por departamento.

26. Requisicion
Columnas:
- NumeroRequision
- FechaRequisicion
- CodigoSucursal
- CodigoEmpleado

Uso:
- Para requisiciones de materiales.

27. Cotizacion
Columnas:
- NumeroRequision
- NumeroCotizacion
- FechaCotizacion
- CodigoProveedore

Uso:
- Para cotizaciones de proveedores.
- IMPORTANTE: la columna se llama CodigoProveedore.

28. Pedido
Columnas:
- NumeroRequision
- NumeroCotizacion
- NumeroPedido

Uso:
- Para pedidos a proveedores.

29. MovimientoMaterial
Columnas:
- CodigoSucursal
- CodigoBodega
- NumeroMovimiento
- FechaMovimiento
- Referencia
- CodigoTipoMovimiento

Uso:
- Para movimientos de bodega e inventario.

30. DetalleMovimientoMaterial
Columnas:
- NumeroMovimiento
- CodigoMaterial
- LineaDetalleMovimiento
- Unidades

Uso:
- Para detalle de movimientos de materiales.

31. TipoMovimiento
Columnas:
- CodigoTipoMovimiento
- Descripcion
- Naturaleza

Uso:
- Para clasificar entradas y salidas de inventario.

EJEMPLOS DE INTERPRETACIÓN:

- Si preguntan por clientes:
  usar Cliente + SocioNegocio.

- Si preguntan por teléfonos de clientes:
  usar Cliente + SocioNegocio + SocioNegocioTelefono.

- Si preguntan por empleados, asesores o mecánicos:
  usar Empleado + SocioNegocio.

- Si preguntan por vehículos:
  usar Automovil.

- Si preguntan por placa:
  usar Automovil.Placa.

- Si preguntan por historial de servicios de un vehículo:
  usar Automovil + Cita + OrdeDeTrabajo + Diagnostico + TipoDiagnostico.

- Si preguntan por órdenes de trabajo:
  usar OrdeDeTrabajo.

- Si preguntan por materiales usados:
  usar DetalleMaterial + Material.

- Si preguntan por mano de obra:
  usar DetalleManoDeObra + ManoObra.

- Si preguntan por ventas:
  usar DocumentoFiscal.ValorTotal.

- Si preguntan por IVA:
  usar DocumentoFiscal.IVA.

- Si preguntan por pagos:
  usar DetallePago + TipoPago.

- Si preguntan por sucursal:
  usar Sucursal.

- Si preguntan por departamento o municipio:
  usar SucursalDireccion + Municipio + Departamento.
"""