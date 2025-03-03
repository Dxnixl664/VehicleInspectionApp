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
                { key: 'air_compressor', value: null },
                { key: 'air_lines', value: null },
                { key: 'battery', value: null },
                { key: 'belts_and_hoses', value: null },
                { key: 'body', value: null },
                { key: 'brake_accessories', value: null },
                { key: 'brake_parking', value: null },
                { key: 'brake_service', value: null },
                { key: 'clutch', value: null },
                { key: 'coupling_devices', value: null } ,
                { key: 'defroster_heater', value: null },
                { key: 'engine', value: null },
                { key: 'exhaust', value: null },
                { key: 'fifth_wheel', value: null },
                { key: 'fluid_levels', value: null },
                { key: 'frame_and_assembly', value: null },
                { key: 'front_axle', value: null },
                { key: 'fuel_tanks', value: null },
                { key: 'horn', value: null },
                { key: 'lights_head_stop', value: null },
                { key: 'lights_tail_dash', value: null },
                { key: 'lights_turn_indicators', value: null },
                { key: 'lights_clearance_marker', value: null },
                { key: 'mirrors', value: null },
                { key: 'muffler', value: null },
                { key: 'oil_pressure', value: null },
                { key: 'radiator', value: null },
                { key: 'rear_end', value: null },
                { key: 'reflectors', value: null },
                { key: 'safety_fire_extinguisher', value: null },
                { key: 'safety_flags_flares_fusees', value: null },
                { key: 'safety_reflective_triangles', value: null },
                { key: 'safety_spare_bulbs_and_fuses', value: null },
                { key: 'safety_spare_seal_beam', value: null },
                { key: 'starter', value: null },
                { key: 'steering', value: null },
                { key: 'suspension_system', value: null },
                { key: 'tire_chains', value: null },
                { key: 'tires', value: null },
                { key: 'transmission', value: null },
                { key: 'trip_recorder', value: null },
                { key: 'wheels_and_rims', value: null },
                { key: 'windows', value: null },
                { key: 'windshield_wipers', value: null },
                { key: 'other', value: null },
            ],
            trailers: [],
            baseTrailerItems: [
                { key: 'brake_connections', value: null },
                { key: 'brakes', value: null },
                { key: 'coupling_devices', value: null },
                { key: 'coupling_king_pin', value: null },
                { key: 'doors', value: null },
                { key: 'hitch', value: null },
                { key: 'landing_gear', value: null },
                { key: 'lights_all', value: null },
                { key: 'reflectors_reflective_tape', value: null },
                { key: 'roof', value: null },
                { key: 'suspension_system', value: null },
                { key: 'tarpaulin', value: null },
                { key: 'tires', value: null },
                { key: 'wheels_and_rims', value: null },
                { key: 'other', value: null },
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
        },
        addTrailer() {
            this.trailers.push({
                trailer_number: '',
                items: JSON.parse(JSON.stringify(this.baseTrailerItems))
            });
        },
        removeTrailer(index) {
            this.trailers.splice(index, 1);
        },
        takeTrailerPhoto(trailerIndex, itemIndex) {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.capture = 'environment';

            fileInput.onchange = (event) => {
                const file = event.target.files[0];
                if (file) {
                    this.trailers[trailerIndex].items[itemIndex].photo = URL.createObjectURL(file);
                }
            };
            fileInput.click();
        },
        async submitInspection () {
            try {
                const token = localStorage.getItem('accessToken');
                if (!token) {
                    alert('Ocurrió su sesión. Inicie sesión nuevamente.');
                    return;
                }

                const truckInspectionItems = {};
                this.truckItems.forEach(item => {
                    truckInspectionItems[item.key] = item.value;
                });

                const trailersData = this.trailers.map((trailer) => {
                    const trailerInspectionItems = {};
                    trailer.items.forEach(tItem => {
                        trailerInspectionItems[tItem.key] = tItem.value;
                    });

                    return {
                        report_id: 0,
                        trailer_number: trailer.trailer_number,
                        inspection_items: trailerInspectionItems
                    };
                });

                const reportData = {
                    carrier: this.selectedCarrier,
                    address: this.address,
                    inspection_date: this.inspectionDate,
                    truck_number: this.truckNumber,
                    odometer_reading: this.odometer,
                    truck_inspection_items: truckInspectionItems,
                    trailers: trailersData
                };

                const response = await fetch('/reports', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'appl'
                    },
                    body: JSON.stringify(reportData)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error al guardar el reporte: ${errorData.detail || response.statusText}`);
                    return;
                }

                alert('Reporte guardado exitosamienta!');
            } catch (error) {
                console.error('Error al enviar el reporte:, error');
                alert('Ocurrió un error al guardar el reporte.')
            }
        }
    }
}).mount('#app')