const { createApp } = Vue

const translations = {
    es: {
        login_title: "Iniciar sesión",
        username_label: "Nombre de usuario",
        username_placeholder: "Ingresa tu usuario",
        password_label: "Contraseña",
        password_placeholder: "Ingresa tu contraseña",
        login_button: "Iniciar sesión",
        start_inspection_button: "INICIAR INSPECCIÓN",
        report_title: "Reporte de inspección de vehículo",
        carrier_label: "Carrier:",
        truckNumber_label: "Número del camión:",
        odometer_label: "Lectura del odómetro:",
        select_carrier: "Selecciona un carrier",
        truckNumber: "Número del camión",
        odometer: "Lectura del odómetro",
        air_compressor: "Compresor de aire",
        air_lines: "Líneas de aire",
        battery: "Batería",
        belts_and_hoses: "Correas y mangueras",
        body: "Carrocería",
        brake_accessories: "Accesorios de freno",
        brake_parking: "Freno de estacionamiento",
        brake_service: "Freno de servicio",
        clutch: "Embrague",
        coupling_devices: "Dispositivos de acoplamiento",
        defroster_heater: "Desempañante/Calefacción",
        engine: "Motor",
        exhaust: "Escape",
        fifth_wheel: "Quinta rueda",
        fluid_levels: "Niveles de fluidos",
        frame_and_assembly: "Chasis y ensamblaje",
        front_axle: "Eje delantero",
        fuel_tanks: "Tanques de combustible",
        horn: "Claxon",
        lights_head_stop: "Luces delanteras y de freno",
        lights_tail_dash: "Luces traseras y del tablero",
        lights_turn_indicators: "Luces direccionales",
        lights_clearance_marker: "Luces de demarcación",
        mirrors: "Espejos",
        muffler: "Silenciador",
        oil_pressure: "Presión de aceite",
        radiator: "Radiador",
        rear_end: "Eje trasero",
        reflectors: "Reflectores",
        safety_fire_extinguisher: "Extintor de incendios",
        safety_flags_flares_fusees: "Banderas/Bengalas/Fusibles de seguridad",
        safety_reflective_triangles: "Triángulos reflectantes de seguridad",
        safety_spare_bulbs_and_fuses: "Bombillas y fusibles de repuesto de seguridad",
        safety_spare_seal_beam: "Foco sellado de repuesto de seguridad",
        starter: "Arranque",
        steering: "Dirección",
        suspension_system: "Sistema de suspensión",
        tire_chains: "Cadenas para neumáticos",
        tires: "Neumáticos",
        transmission: "Transmisión (caja de cambios)",
        trip_recorder: "Registrador de viaje",
        wheels_and_rims: "Ruedas y llantas",
        windows: "Ventanas",
        windshield_wipers: "Limpiaparabrisas",
        other: "Otros"
    },
    en: {
        login_title: "Login",
        username_label: "Username",
        username_placeholder: "Enter your username",
        password_label: "Password",
        password_placeholder: "Enter your password",
        login_button: "Log In",
        start_inspection_button: "START INSPECTION",
        report_title: "Vehicle Inspection Report",
        carrier_label: "Carrier:",
        truckNumber_label: "Truck Number:",
        odometer_label: "Odometer Reading:",
        select_carrier: "Select a carrier",
        truckNumber: "Truck Number",
        odometer: "Odometer reading",
        air_compressor: "Air compressor",
        air_lines: "Air lines",
        battery: "Battery",
        belts_and_hoses: "Belts and hoses",
        body: "Body",
        brake_accessories: "Brake accessories",
        brake_parking: "Parking brake",
        brake_service: "Service brake",
        clutch: "Clutch",
        coupling_devices: "Coupling devices",
        defroster_heater: "Defroster/Heater",
        engine: "Engine",
        exhaust: "Exhaust",
        fifth_wheel: "Fifth wheel",
        fluid_levels: "Fluid levels",
        frame_and_assembly: "Frame and assembly",
        front_axle: "Front axle",
        fuel_tanks: "Fuel tanks",
        horn: "Horn",
        lights_head_stop: "Head and stop lights",
        lights_tail_dash: "Tail and dash lights",
        lights_turn_indicators: "Turn indicators",
        lights_clearance_marker: "Clearance marker lights",
        mirrors: "Mirrors",
        muffler: "Muffler",
        oil_pressure: "Oil pressure",
        radiator: "Radiator",
        rear_end: "Rear end",
        reflectors: "Reflectors",
        safety_fire_extinguisher: "Fire extinguisher",
        safety_flags_flares_fusees: "Flags/Flares/Fusees",
        safety_reflective_triangles: "Reflective triangles",
        safety_spare_bulbs_and_fuses: "Spare bulbs and fuses",
        safety_spare_seal_beam: "Spare sealed beam",
        starter: "Starter",
        steering: "Steering",
        suspension_system: "Suspension system",
        tire_chains: "Tire chains",
        tires: "Tires",
        transmission: "Transmission",
        trip_recorder: "Trip recorder",
        wheels_and_rims: "Wheels and rims",
        windows: "Windows",
        windshield_wipers: "Windshield wipers",
        other: "Other"
    }
};

createApp({
    data() {
        return {
            username: '',
            password: '',
            isLoggedIn: false,
            userRole: null,
            isInspectionStarted: false,
            selectedLanguage: 'es',
            carriers: [
                'DFC - Duran Freight Corp',
                'DFCTL - DFC Transportation and Logistics',
                'DFCLS - DFC Logistics Solutions',
                'PFM - Premium Freight de México'
            ],
            selectedCarrier: '',
            address: '',
            inspectionDate: null,
            truckNumber: '',
            odometer: '',
            truckItems: []
        };
    },
    mounted() {
        this.initializeTruckItems();
    },
    methods: {
        initializeTruckItems() {
            this.truckItems = Object.keys(translations.es).filter(key => key !== 'carrier' && key !== 'truckNumber' && key !== 'odometer').map(key => ({
                key,
                label: this.translateText(key),
                value: null
            }));
        },
        translateText(key) {
            return translations[this.selectedLanguage][key] || key;
        },
        changeLanguage() {
            this.truckItems.forEach(item => {
                item.label = this.translateText(item.key);
            });
        },
        async login() {
            try {
                const response = await fetch('/users/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail || 'Credenciales inválidas'}`);
                    return;
                }

                const data = await response.json();
                localStorage.setItem('accessToken', data.access_token);
                localStorage.setItem('tokenType', data.token_type);

                this.isLoggedIn = true;
                this.userRole = data.role;
            } catch (error) {
                console.error('Error en la solicitud de inicio de sesión:', error);
                alert('Ocurrió un error al intentar iniciar sesión');
            }
        },
        startInspection() {
            this.isInspectionStarted = true;
            this.getLocation();
            const now = new Date();
            this.inspectionDate = `${now.toISOString().slice(0, 10)} ${now.toTimeString().slice(0, 8)}`;
        },
        async getLocation() {
            if ('geolocation' in navigator) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const { latitude, longitude } = position.coords;
                        this.address = `Lat: ${latitude}, Lng: ${longitude}`;
                    },
                    (error) => {
                        console.error('Error obteniendo geolocalización:', error);
                        alert('No se pudo obtener la ubicación.');
                    },
                    { enableHighAccuracy: true }
                );
            } else {
                alert('La geolocalización no está soportada en este navegador.');
            }
        },
        takePhoto(index) {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.capture = 'environment';
    
            fileInput.onchange = (event) => {
                const file = event.target.files[0];
                if (file) {
                    this.truckItems[index].photo = URL.createObjectURL(file);
                }
            };
    
            fileInput.click();
        },
    
        removePhoto(index) {
            this.truckItems[index].photo = null;  // Limpia la foto del ítem correspondiente
        }
    }
    
}).mount('#app');
