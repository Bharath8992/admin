// Membership functionality
document.addEventListener('DOMContentLoaded', function() {
    // Upgrade membership
    const upgradeBtn = document.getElementById('upgradeMembership');
    if (upgradeBtn) {
        upgradeBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to upgrade to Premium membership?')) {
                alert('Membership upgraded successfully!');
            }
        });
    }

    // Update membership
    const updateBtn = document.getElementById('updateMembership');
    if (updateBtn) {
        updateBtn.addEventListener('click', function() {
            const userSearch = document.getElementById('userSearch').value;
            const membershipType = document.getElementById('membershipType').value;
            
            if (!userSearch) {
                alert('Please enter a user to update');
                return;
            }
            
            alert(`Membership updated to ${membershipType} for user: ${userSearch}`);
        });
    }
});