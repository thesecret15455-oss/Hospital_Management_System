-- =====================================================================
-- Bulk data insert for hospital_management_system
-- Generated from provided CSV exports. Run AFTER the schema-creation
-- script (Hospital_management_system_sql_querries.sql) has been executed.
-- =====================================================================

USE hospital_management_system;

-- ---------------------------------------------------------------
-- Users
-- ---------------------------------------------------------------
INSERT INTO Users (user_id, username, password_hash, role, email, phone, created_at, is_active) VALUES
(1, 'admin_john', 'hashed_pwd_1', 'Admin', 'john.d''souza@hospital.com', '9800000001', '2023-01-05 09:00:00', 1),
(2, 'admin_mary', 'hashed_pwd_2', 'Admin', 'mary.fernandes@hospital.com', '9800000002', '2023-01-05 09:00:00', 1),
(3, 'admin_peter', 'hashed_pwd_3', 'Admin', 'peter.rodrigues@hospital.com', '9800000003', '2023-01-05 09:00:00', 1),
(4, 'admin_alice', 'hashed_pwd_4', 'Admin', 'alice.fonseca@hospital.com', '9800000004', '2023-01-05 09:00:00', 1),
(5, 'admin_steve', 'hashed_pwd_5', 'Admin', 'steve.pinto@hospital.com', '9800000005', '2023-01-05 09:00:00', 1),
(6, 'admin_grace', 'hashed_pwd_6', 'Admin', 'grace.almeida@hospital.com', '9800000006', '2023-01-05 09:00:00', 1),
(7, 'admin_tom', 'hashed_pwd_7', 'Admin', 'tom.coelho@hospital.com', '9800000007', '2023-01-05 09:00:00', 1),
(8, 'admin_nancy', 'hashed_pwd_8', 'Admin', 'nancy.rebello@hospital.com', '9800000008', '2023-01-05 09:00:00', 1),
(9, 'admin_paul', 'hashed_pwd_9', 'Admin', 'paul.vaz@hospital.com', '9800000009', '2023-01-05 09:00:00', 1),
(10, 'admin_diana', 'hashed_pwd_10', 'Admin', 'diana.lobo@hospital.com', '9800000010', '2023-01-05 09:00:00', 1),
(11, 'dr_ravi', 'hashed_pwd_11', 'Doctor', 'ravi.sharma@hospital.com', '9800000011', '2023-02-01 10:00:00', 1),
(12, 'dr_anjali', 'hashed_pwd_12', 'Doctor', 'anjali.verma@hospital.com', '9800000012', '2023-02-01 10:00:00', 1),
(13, 'dr_suresh', 'hashed_pwd_13', 'Doctor', 'suresh.iyer@hospital.com', '9800000013', '2023-02-01 10:00:00', 1),
(14, 'dr_neha', 'hashed_pwd_14', 'Doctor', 'neha.kapoor@hospital.com', '9800000014', '2023-02-01 10:00:00', 1),
(15, 'dr_amit', 'hashed_pwd_15', 'Doctor', 'amit.joshi@hospital.com', '9800000015', '2023-02-01 10:00:00', 1),
(16, 'dr_priya', 'hashed_pwd_16', 'Doctor', 'priya.nair@hospital.com', '9800000016', '2023-02-01 10:00:00', 1),
(17, 'dr_vikram', 'hashed_pwd_17', 'Doctor', 'vikram.singh@hospital.com', '9800000017', '2023-02-01 10:00:00', 1),
(18, 'dr_sneha', 'hashed_pwd_18', 'Doctor', 'sneha.reddy@hospital.com', '9800000018', '2023-02-01 10:00:00', 1),
(19, 'dr_karan', 'hashed_pwd_19', 'Doctor', 'karan.malhotra@hospital.com', '9800000019', '2023-02-01 10:00:00', 1),
(20, 'dr_divya', 'hashed_pwd_20', 'Doctor', 'divya.menon@hospital.com', '9800000020', '2023-02-01 10:00:00', 1),
(21, 'pat_rahul', 'hashed_pwd_21', 'Patient', 'rahul.gupta@gmail.com', '9800000121', '2023-03-01 11:00:00', 1),
(22, 'pat_sonal', 'hashed_pwd_22', 'Patient', 'sonal.patel@gmail.com', '9800000122', '2023-03-01 11:00:00', 1),
(23, 'pat_arjun', 'hashed_pwd_23', 'Patient', 'arjun.rao@gmail.com', '9800000123', '2023-03-01 11:00:00', 1),
(24, 'pat_meera', 'hashed_pwd_24', 'Patient', 'meera.das@gmail.com', '9800000124', '2023-03-01 11:00:00', 1),
(25, 'pat_vivek', 'hashed_pwd_25', 'Patient', 'vivek.chauhan@gmail.com', '9800000125', '2023-03-01 11:00:00', 1),
(26, 'pat_kavya', 'hashed_pwd_26', 'Patient', 'kavya.pillai@gmail.com', '9800000126', '2023-03-01 11:00:00', 1),
(27, 'pat_rohan', 'hashed_pwd_27', 'Patient', 'rohan.mehta@gmail.com', '9800000127', '2023-03-01 11:00:00', 1),
(28, 'pat_ishita', 'hashed_pwd_28', 'Patient', 'ishita.bose@gmail.com', '9800000128', '2023-03-01 11:00:00', 1),
(29, 'pat_aditya', 'hashed_pwd_29', 'Patient', 'aditya.kulkarni@gmail.com', '9800000129', '2023-03-01 11:00:00', 1),
(30, 'pat_pooja', 'hashed_pwd_30', 'Patient', 'pooja.bhatt@gmail.com', '9800000130', '2023-03-01 11:00:00', 1);

-- ---------------------------------------------------------------
-- Departments  (head_doctor_id filled in later via UPDATE, since it
-- references Doctors which doesn't exist yet)
-- ---------------------------------------------------------------
INSERT INTO Departments (department_id, department_name, head_doctor_id) VALUES
(1, 'Cardiology', NULL),
(2, 'Neurology', NULL),
(3, 'Orthopedics', NULL),
(4, 'Pediatrics', NULL),
(5, 'Dermatology', NULL),
(6, 'ENT', NULL),
(7, 'Gynecology', NULL),
(8, 'Psychiatry', NULL),
(9, 'General Medicine', NULL),
(10, 'Ophthalmology', NULL);

-- ---------------------------------------------------------------
-- Doctors
-- ---------------------------------------------------------------
INSERT INTO Doctors (doctor_id, user_id, first_name, last_name, specialization, qualification, experience_years, department_id, consultation_fee) VALUES
(1, 11, 'Ravi', 'Sharma', 'Cardiologist', 'MBBS, MD', 12, 1, 800),
(2, 12, 'Anjali', 'Verma', 'Neurologist', 'MBBS, DM', 9, 2, 900),
(3, 13, 'Suresh', 'Iyer', 'Orthopedic Surgeon', 'MBBS, MS', 15, 3, 1000),
(4, 14, 'Neha', 'Kapoor', 'Pediatrician', 'MBBS, DCH', 7, 4, 600),
(5, 15, 'Amit', 'Joshi', 'Dermatologist', 'MBBS, DDVL', 10, 5, 700),
(6, 16, 'Priya', 'Nair', 'ENT Specialist', 'MBBS, MS(ENT)', 6, 6, 650),
(7, 17, 'Vikram', 'Singh', 'Gynecologist', 'MBBS, DGO', 11, 7, 850),
(8, 18, 'Sneha', 'Reddy', 'Psychiatrist', 'MBBS, MD(Psych)', 8, 8, 900),
(9, 19, 'Karan', 'Malhotra', 'General Physician', 'MBBS', 5, 9, 500),
(10, 20, 'Divya', 'Menon', 'Ophthalmologist', 'MBBS, MS(Ophtho)', 14, 10, 750);

-- ---------------------------------------------------------------
-- Now that Doctors exist, set each department's head doctor
-- ---------------------------------------------------------------
UPDATE Departments SET head_doctor_id = 1 WHERE department_id = 1;
UPDATE Departments SET head_doctor_id = 2 WHERE department_id = 2;
UPDATE Departments SET head_doctor_id = 3 WHERE department_id = 3;
UPDATE Departments SET head_doctor_id = 4 WHERE department_id = 4;
UPDATE Departments SET head_doctor_id = 5 WHERE department_id = 5;
UPDATE Departments SET head_doctor_id = 6 WHERE department_id = 6;
UPDATE Departments SET head_doctor_id = 7 WHERE department_id = 7;
UPDATE Departments SET head_doctor_id = 8 WHERE department_id = 8;
UPDATE Departments SET head_doctor_id = 9 WHERE department_id = 9;
UPDATE Departments SET head_doctor_id = 10 WHERE department_id = 10;

-- ---------------------------------------------------------------
-- Patients
-- ---------------------------------------------------------------
INSERT INTO Patients (patient_id, user_id, first_name, last_name, dob, gender, blood_group, address, emergency_contact_name, emergency_contact_phone, registration_date) VALUES
(1, 21, 'Rahul', 'Gupta', '1990-05-14', 'Male', 'O+', '12 MG Road, Pune', 'Suresh Gupta', '9810000001', '2023-04-01 09:00:00'),
(2, 22, 'Sonal', 'Patel', '1985-11-02', 'Female', 'A+', '45 Baner St, Pune', 'Anil Patel', '9810000002', '2023-04-01 09:00:00'),
(3, 23, 'Arjun', 'Rao', '1998-07-23', 'Male', 'B+', '7 Kothrud Ave, Pune', 'Radha Rao', '9810000003', '2023-04-01 09:00:00'),
(4, 24, 'Meera', 'Das', '1975-03-30', 'Female', 'AB+', '23 Wakad Rd, Pune', 'Deepak Das', '9810000004', '2023-04-01 09:00:00'),
(5, 25, 'Vivek', 'Chauhan', '2001-01-19', 'Male', 'O-', '9 Hinjewadi Ln, Pune', 'Sunita Chauhan', '9810000005', '2023-04-01 09:00:00'),
(6, 26, 'Kavya', 'Pillai', '1993-09-09', 'Female', 'A-', '31 Aundh St, Pune', 'Manoj Pillai', '9810000006', '2023-04-01 09:00:00'),
(7, 27, 'Rohan', 'Mehta', '1988-12-25', 'Male', 'B-', '18 Viman Nagar, Pune', 'Geeta Mehta', '9810000007', '2023-04-01 09:00:00'),
(8, 28, 'Ishita', 'Bose', '1996-06-17', 'Female', 'AB-', '5 Kondhwa Rd, Pune', 'Ramesh Bose', '9810000008', '2023-04-01 09:00:00'),
(9, 29, 'Aditya', 'Kulkarni', '1979-04-11', 'Male', 'O+', '27 Hadapsar Ln, Pune', 'Latha Kulkarni', '9810000009', '2023-04-01 09:00:00'),
(10, 30, 'Pooja', 'Bhatt', '2003-02-28', 'Female', 'A+', '14 Shivaji Nagar, Pune', 'Vinay Bhatt', '9810000010', '2023-04-01 09:00:00');

-- ---------------------------------------------------------------
-- Admins
-- ---------------------------------------------------------------
INSERT INTO Admins (admin_id, user_id, first_name, last_name, designation) VALUES
(1, 1, 'John', 'D''Souza', 'Hospital Administrator'),
(2, 2, 'Mary', 'Fernandes', 'Assistant Administrator'),
(3, 3, 'Peter', 'Rodrigues', 'IT Administrator'),
(4, 4, 'Alice', 'Fonseca', 'HR Administrator'),
(5, 5, 'Steve', 'Pinto', 'Finance Administrator'),
(6, 6, 'Grace', 'Almeida', 'Front Desk Administrator'),
(7, 7, 'Tom', 'Coelho', 'Records Administrator'),
(8, 8, 'Nancy', 'Rebello', 'Operations Administrator'),
(9, 9, 'Paul', 'Vaz', 'Billing Administrator'),
(10, 10, 'Diana', 'Lobo', 'Inventory Administrator');

-- ---------------------------------------------------------------
-- Doctor_Schedule
-- ---------------------------------------------------------------
INSERT INTO Doctor_Schedule (schedule_id, doctor_id, day_of_week, start_time, end_time) VALUES
(1, 1, 'Mon', '09:00:00', '13:00:00'),
(2, 2, 'Tue', '10:00:00', '14:00:00'),
(3, 3, 'Wed', '09:30:00', '13:30:00'),
(4, 4, 'Thu', '11:00:00', '15:00:00'),
(5, 5, 'Fri', '09:00:00', '13:00:00'),
(6, 6, 'Mon', '10:30:00', '14:30:00'),
(7, 7, 'Tue', '09:00:00', '13:00:00'),
(8, 8, 'Wed', '10:00:00', '14:00:00'),
(9, 9, 'Thu', '11:30:00', '15:30:00'),
(10, 10, 'Fri', '09:00:00', '13:00:00');

-- ---------------------------------------------------------------
-- Appointments
-- ---------------------------------------------------------------
INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status, reason_for_visit, created_at) VALUES
(1, 1, 1, '2024-06-01', '09:15:00', 'Completed', 'Chest pain', '2024-06-01 08:00:00'),
(2, 2, 2, '2024-06-02', '10:15:00', 'Completed', 'Migraine', '2024-06-02 08:00:00'),
(3, 3, 3, '2024-06-03', '09:45:00', 'Completed', 'Knee pain', '2024-06-03 08:00:00'),
(4, 4, 4, '2024-06-04', '11:15:00', 'Completed', 'Child fever', '2024-06-04 08:00:00'),
(5, 5, 5, '2024-06-05', '09:15:00', 'Completed', 'Skin rash', '2024-06-05 08:00:00'),
(6, 6, 6, '2024-06-06', '10:45:00', 'Completed', 'Ear infection', '2024-06-06 08:00:00'),
(7, 7, 7, '2024-06-07', '09:15:00', 'Completed', 'Routine checkup', '2024-06-07 08:00:00'),
(8, 8, 8, '2024-06-08', '10:15:00', 'Completed', 'Anxiety', '2024-06-08 08:00:00'),
(9, 9, 9, '2024-06-09', '11:45:00', 'Completed', 'General fever', '2024-06-09 08:00:00'),
(10, 10, 10, '2024-06-10', '09:15:00', 'Completed', 'Eye strain', '2024-06-10 08:00:00'),
(11, 1, 1, '2024-06-11', '10:00:00', 'Scheduled', 'Follow-up consultation', '2024-06-11 08:00:00'),
(12, 2, 2, '2024-06-12', '11:00:00', 'Cancelled', 'Routine checkup', '2024-06-12 08:00:00');

-- ---------------------------------------------------------------
-- Medical_Records
-- ---------------------------------------------------------------
INSERT INTO Medical_Records (record_id, patient_id, doctor_id, appointment_id, diagnosis, treatment, notes, record_date) VALUES
(1, 1, 1, 1, 'Mild Angina', 'Prescribed medication & ECG follow-up', 'Patient advised to monitor BP', '2024-06-01 12:00:00'),
(2, 2, 2, 2, 'Chronic Migraine', 'Prescribed pain relief & rest', 'Avoid triggers like bright light', '2024-06-02 12:00:00'),
(3, 3, 3, 3, 'Osteoarthritis', 'Physiotherapy recommended', 'Review after 3 weeks', '2024-06-03 12:00:00'),
(4, 4, 4, 4, 'Viral Fever', 'Antipyretics & rest advised', 'Recovered within a week', '2024-06-04 12:00:00'),
(5, 5, 5, 5, 'Contact Dermatitis', 'Topical ointment prescribed', 'Avoid known allergens', '2024-06-05 12:00:00'),
(6, 6, 6, 6, 'Otitis Media', 'Antibiotics prescribed', 'Review after 5 days', '2024-06-06 12:00:00'),
(7, 7, 7, 7, 'Healthy - No Issues', 'Advised routine diet & exercise', 'Annual checkup recommended', '2024-06-07 12:00:00'),
(8, 8, 8, 8, 'Generalized Anxiety Disorder', 'Counselling recommended', 'Referred for follow-up therapy', '2024-06-08 12:00:00'),
(9, 9, 9, 9, 'Viral Fever', 'Antipyretics & fluids advised', 'Stable, no complications', '2024-06-09 12:00:00'),
(10, 10, 10, 10, 'Digital Eye Strain', '20-20-20 rule advised, lubricant drops', 'Reduce screen time', '2024-06-10 12:00:00');

-- ---------------------------------------------------------------
-- Prescriptions
-- ---------------------------------------------------------------
INSERT INTO Prescriptions (prescription_id, record_id, medicine_name, dosage, duration, instructions) VALUES
(1, 1, 'Aspirin 75mg', 'Once daily', '30 days', 'Take after breakfast'),
(2, 2, 'Naproxen 250mg', 'Twice daily', '7 days', 'Take after meals'),
(3, 3, 'Glucosamine 500mg', 'Twice daily', '60 days', 'Take with milk'),
(4, 4, 'Paracetamol 500mg', 'Thrice daily', '5 days', 'Take if fever exceeds 100F'),
(5, 5, 'Hydrocortisone Cream', 'Apply twice daily', '10 days', 'Avoid sun exposure after application'),
(6, 6, 'Amoxicillin 500mg', 'Thrice daily', '7 days', 'Complete full course'),
(7, 7, 'Multivitamin', 'Once daily', '30 days', 'Take with breakfast'),
(8, 8, 'Sertraline 50mg', 'Once daily', '90 days', 'Do not discontinue abruptly'),
(9, 9, 'Paracetamol 650mg', 'Thrice daily', '5 days', 'Take with food'),
(10, 10, 'Lubricant Eye Drops', 'As needed', '30 days', 'Use for dry/strained eyes');

-- ---------------------------------------------------------------
-- Billing
-- ---------------------------------------------------------------
INSERT INTO Billing (bill_id, patient_id, appointment_id, amount, payment_status, payment_date, payment_method) VALUES
(1, 1, 1, 800, 'Paid', '2024-06-01', 'Card'),
(2, 2, 2, 900, 'Paid', '2024-06-02', 'Cash'),
(3, 3, 3, 1000, 'Paid', '2024-06-03', 'UPI'),
(4, 4, 4, 600, 'Paid', '2024-06-04', 'Cash'),
(5, 5, 5, 700, 'Paid', '2024-06-05', 'Card'),
(6, 6, 6, 650, 'Paid', '2024-06-06', 'UPI'),
(7, 7, 7, 850, 'Paid', '2024-06-07', 'Cash'),
(8, 8, 8, 900, 'Paid', '2024-06-08', 'Card'),
(9, 9, 9, 500, 'Paid', '2024-06-09', 'UPI'),
(10, 10, 10, 750, 'Paid', '2024-06-10', 'Cash'),
(11, 1, 11, 800, 'Pending', NULL, NULL),
(12, 2, 12, 0, 'Pending', NULL, NULL);