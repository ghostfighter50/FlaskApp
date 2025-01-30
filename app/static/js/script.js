function toggleInterface(target) {
    const wrapper = document.getElementById('wrapper');
    if (target === 'student') {
        wrapper.style.transform = 'translateX(0)';
    } else if (target === 'professor') {
        wrapper.style.transform = 'translateX(-33.33%)';
    } else if (target === 'director') {
        wrapper.style.transform = 'translateX(-66.66%)';
    }
}

