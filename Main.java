public static void main(String[] args) {
    SistemaLogistica sistema = new SistemaLogistica();

    // Configuración del Grafo de la Ciudad
    sistema.getMapaCiudad().agregarConexion("Centro", "Avenida 1", 5);
    sistema.getMapaCiudad().agregarConexion("Avenida 1", "Zona Norte", 10);
    sistema.getMapaCiudad().agregarConexion("Centro", "Zona Sur", 4);
    sistema.getMapaCiudad().agregarConexion("Zona Sur", "Zona Este", 3);

    // Aqui registramos repartidores con diferentes vehículos colocados en distintas zonas
    Repartidor rep1 = new Repartidor("Marcos", new Moto(), "Avenida 1");
    Repartidor rep2 = new Repartidor("Elena", new Camion(), "Zona Sur");
    
    sistema.registrarRepartidor(rep1);
    sistema.registrarRepartidor(rep2);

    System.out.println("Asignacion inteligente"); // Pruebas FASE 3

    // Aqui se crean paquetes con diferentes destinos
    Paquete paqueteNorte = new Paquete("A789", 1.5, "Zona Norte", "CLI01");
    Paquete paqueteEste = new Paquete("B456", 14.0, "Zona Este", "CLI02");

    // Procesamos de forma automática
    // Marcos (Moto) está en Avenida 1 (más cerca de Zona Norte) -> Debería quedarse este paquete
    sistema.procesarAsignacionInteligente(paqueteNorte);

    // Elena (Camión) está en Zona Sur (más cerca de Zona Este) -> Debería quedarse este paquete
    sistema.procesarAsignacionInteligente(paqueteEste);
    
    System.out.println("\n=================================================");
}
