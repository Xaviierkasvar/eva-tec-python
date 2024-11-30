import React, { useState, useEffect } from "react";
import axios from "axios";
import Swal from "sweetalert2";
import { Table, Form, Button, Row, Col, Container, Pagination } from "react-bootstrap";
import * as XLSX from "xlsx";

const EventLog = ({ token }) => {
  const [filters, setFilters] = useState({
    startDate: "",
    endDate: "",
    type: "",
    description: "",
  });
  const [logs, setLogs] = useState([]);
  const [hasQueried, setHasQueried] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalRecords, setTotalRecords] = useState(null); // Variable para almacenar total_records

  useEffect(() => {
    if (hasQueried) {
      fetchLogs();
    }
  }, [currentPage, pageSize]);

  const fetchLogs = async () => {
    setIsLoading(true);
    try {
      const { startDate, endDate, type, description } = filters;

      const response = await axios.get("http://127.0.0.1:8000/history", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          start_date: startDate || undefined,
          end_date: endDate || undefined,
          type: type || undefined,
          description: description || undefined,
          page: currentPage,
          page_size: pageSize === "all" ? undefined : pageSize,
        },
      });

      if (response.data.status === "success") {
        setLogs(response.data.data);
        setTotalPages(response.data.total_pages);
        setTotalRecords(response.data.total_records); // Actualizamos total_records
        setHasQueried(true);
      } else {
        Swal.fire({
          icon: "error",
          title: "Error al cargar datos",
          text: "No se pudo obtener el registro de eventos.",
        });
      }
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error de servidor",
        text: "Hubo un problema al comunicarse con el servidor.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const exportToExcel = () => {
    if (!hasQueried) {
      Swal.fire({
        icon: "info",
        title: "Consulta requerida",
        text: "Debe realizar una consulta antes de exportar.",
      });
      return;
    }

    const worksheet = XLSX.utils.json_to_sheet(logs);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Logs");
    XLSX.writeFile(workbook, "logs.xlsx");

    Swal.fire({
      icon: "success",
      title: "Exportación",
      text: "Los datos se han exportado exitosamente a Excel.",
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handlePageSizeChange = (e) => {
    setPageSize(e.target.value);
    setCurrentPage(1); // Reset to first page when page size changes
  };

  return (
    <Container className="mt-4">
      <h2 className="text-center mb-4">Registro de Eventos</h2>

      {/* Formulario de Filtros */}
      <Form className="mb-4 text-center">
        <Row>
          <Col md={3} className="mb-3">
            <Form.Group controlId="startDate">
              <Form.Label>Fecha de Inicio</Form.Label>
              <Form.Control
                type="datetime-local"
                name="startDate"
                value={filters.startDate}
                onChange={handleInputChange}
              />
            </Form.Group>
          </Col>
          <Col md={3} className="mb-3">
            <Form.Group controlId="endDate">
              <Form.Label>Fecha de Fin</Form.Label>
              <Form.Control
                type="datetime-local"
                name="endDate"
                value={filters.endDate}
                onChange={handleInputChange}
              />
            </Form.Group>
          </Col>
          <Col md={3} className="mb-3">
            <Form.Group controlId="type">
              <Form.Label>Filtrar por Tipo</Form.Label>
              <Form.Select
                name="type"
                value={filters.type}
                onChange={handleInputChange}
              >
                <option value="">Todos</option>
                <option value="CARGA_DOCUMENTO">Carga de documento</option>
                <option value="IA">IA</option>
                <option value="INTERACCION_USUARIO">Interacción del usuario</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={3} className="mb-3">
            <Form.Group controlId="description">
              <Form.Label>Descripción</Form.Label>
              <Form.Control
                type="text"
                name="description"
                maxLength={10}
                value={filters.description}
                onChange={handleInputChange}
              />
            </Form.Group>
          </Col>
        </Row>
        <Row>
          <Col md={3} className="mb-3 justify-content-start">
            <Button variant="primary" onClick={fetchLogs} disabled={isLoading}>
              {isLoading ? "Consultando..." : "Consultar"}
            </Button>{" "}
            <Button variant="success" onClick={exportToExcel} disabled={isLoading}>
              {isLoading ? "Exportando..." : "Exportar a Excel"}
            </Button>
          </Col>
          <Col md={6}></Col>
          <Col md={3} className="mb-3 justify-content-end">
            <Form.Group controlId="pageSize">
              <Form.Label>Registros por página</Form.Label>
              <Form.Select
                name="pageSize"
                value={pageSize}
                onChange={handlePageSizeChange}
              >
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="30">30</option>
                <option value="50">50</option>
                <option value="100">100</option>
                {/* Si totalRecords está disponible, usamos ese valor, si no, usamos 500 */}
                <option value={totalRecords || 500}>All</option>
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>
      </Form>

      {/* Tabla de Resultados */}
      <Table striped bordered hover responsive className="text-center">
        <thead className="text-center">
          <tr>
            <th>ID</th>
            <th>Tipo</th>
            <th>Descripción</th>
            <th>Fecha y Hora</th>
          </tr>
        </thead>
        <tbody>
          {logs.length > 0 ? (
            logs.map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.type}</td>
                <td className="text-start">{log.description}</td>
                <td>{new Date(log.datetime).toLocaleString()}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4">No hay registros para mostrar.</td>
            </tr>
          )}
        </tbody>
      </Table>

      {/* Paginación */}
      {pageSize !== "all" && (
        <Pagination className="justify-content-center mt-4">
          {[...Array(totalPages).keys()].map((page) => (
            <Pagination.Item
              key={page + 1}
              active={page + 1 === currentPage}
              onClick={() => handlePageChange(page + 1)}
            >
              {page + 1}
            </Pagination.Item>
          ))}
        </Pagination>
      )}
    </Container>
  );
};

export default EventLog;
