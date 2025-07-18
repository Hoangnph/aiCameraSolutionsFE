const bcrypt = require('bcryptjs');

async function generateHash() {
    const password = 'Admin123!';
    const hash = await bcrypt.hash(password, 12);
    console.log('Password:', password);
    console.log('Hash:', hash);
    
    // Test verification
    const isValid = await bcrypt.compare(password, hash);
    console.log('Verification:', isValid);
}

generateHash().catch(console.error); 