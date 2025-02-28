const { createApp } = Vue

createApp({
    data() {
        return {
            username: '',
            password: '',
            isLoggedIn: false,
            userRole: null,

            isInspectionStarted: false,
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
            odometer: 0,
            truckItems: [
                { key: 'air_compressor',                label: 'Compresor de aire',                             value: null },
                { key: 'air_lines',                     label: 'Líneas de aire',                                value: null },
                { key: 'battery',                       label: 'Batería',                                       value: null },
                { key: 'belts_and_hoses',               label: 'Correas y mangueras',                           value: null },
                { key: 'body',                          label: 'Carrocería',                                    value: null },
                { key: 'brake_accessories',             label: 'Accesorios de freno',                           value: null },
                { key: 'brake_parking',                 label: 'Freno de estacionamiento',                      value: null },
                { key: 'brake_service',                 label: 'Freno de servicio',                             value: null },
                { key: 'clutch',                        label: 'Embrague',                                      value: null },
                { key: 'coupling_devices',              label: 'Dispositivos de acoplamiento',                  value: null } ,
                { key: 'defroster_heater',              label: 'Desempañante/Calefacción',                      value: null },
                { key: 'engine',                        label: 'Motor',                                         value: null },
                { key: 'exhaust',                       label: 'Escape',                                        value: null },
                { key: 'fifth_wheel',                   label: 'Quinta rueda',                                  value: null },
                { key: 'fluid_levels',                  label: 'Niveles de fluidos',                            value: null },
                { key: 'frame_and_assembly',            label: 'Chasis y ensamblaje',                           value: null },
                { key: 'front_axle',                    label: 'Eje delantero',                                 value: null },
                { key: 'fuel_tanks',                    label: 'Tanques de combustible',                        value: null },
                { key: 'horn',                          label: 'Claxon',                                        value: null },
                { key: 'lights_head_stop',              label: 'Luces delanteras y de freno',                   value: null },
                { key: 'lights_tail_dash',              label: 'Luces traseras y del tablero',                  value: null },
                { key: 'lights_turn_indicators',        label: 'Luces direccionales',                           value: null },
                { key: 'lights_clearance_marker',       label: 'Luces de demarcación',                          value: null },
                { key: 'mirrors',                       label: 'Espejos',                                       value: null },
                { key: 'muffler',                       label: 'Silenciador',                                   value: null },
                { key: 'oil_pressure',                  label: 'Presión de aceite',                             value: null },
                { key: 'radiator',                      label: 'Radiador',                                      value: null },
                { key: 'rear_end',                      label: 'Eje trasero',                                   value: null },
                { key: 'reflectors',                    label: 'Reflectores',                                   value: null },
                { key: 'safety_fire_extinguisher',      label: 'Extintor de incendios',                         value: null },
                { key: 'safety_flags_flares_fusees',    label: 'Banderas/Bengalas/Fusibles de seguridad',       value: null },
                { key: 'safety_reflective_triangles',   label: 'Triángulos reflectantes de seguridad',          value: null },
                { key: 'safety_spare_bulbs_and_fuses',  label: 'Bombillas y fusibles de repuesto de seguridad', value: null },
                { key: 'safety_spare_seal_beam',        label: 'Foco sellado de repuesto de seguridad',         value: null },
                { key: 'starter',                       label: 'Arranque',                                      value: null },
                { key: 'steering',                      label: 'Dirección',                                     value: null },
                { key: 'suspension_system',             label: 'Sistema de suspensión',                         value: null },
                { key: 'tire_chains',                   label: 'Cadenas para neumáticos',                       value: null },
                { key: 'tires',                         label: 'Neumáticos',                                    value: null },
                { key: 'transmission',                  label: 'Transmisión (caja de cambios)',                 value: null },
                { key: 'trip_recorder',                 label: 'Registrador de viaje',                          value: null },
                { key: 'wheels_and_rims',               label: 'Ruedas y llantas',                              value: null },
                { key: 'windows',                       label: 'Ventanas',                                      value: null },
                { key: 'windshield_wipers',             label: 'Limpiaparabrisas',                              value: null },
                { key: 'other',                         label: 'Otros',                                         value: null },
            ]
        }
    },
    watch: {
        odometer(newVal) {
            if (newVal < 0) {
                this.odometer = 0;
            }
        },
    },
    methods: {
        async login() {
            try {
                const response = await fetch('/users/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
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

                this.isLoggedIn = true
                this.userRole = data.role

            } catch (error) {
                console.error('Error en la solicitud de inicio de sesión: ', error);
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
                navigator.geolocation.getCurrentPosition((position) => {
                    const { latitude, longitude } = position.coords;
                    this.address = `Lat: ${latitude}, Lng: ${longitude}`;
                },
                (error) => {
                    console.error('Error obteniendo geolocalización:', error);
                    alert('No se pudo obtener la ubicación.');
                },
                { enableHighAccuracy: true}
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
                    // Guardar localmente
                    this.truckItems[index].photo = URL.createObjectURL(file);

                    /* TODO Subir a servidor
                    const formData = new FormData();
                    formData.append('photo', file);
                    fetch('/upload-endpoint', {
                        method: 'POST',
                        body: formData
                    })
                    .then(
                        TODO
                     );
                    * */
                }
            };

            fileInput.click();
        },
        preventNegative() {
            if (this.odometer < 0) {
                this.odometer = 0;
            }
        }
    }
}).mount('#app')