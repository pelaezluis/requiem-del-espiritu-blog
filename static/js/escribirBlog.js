function escribirBlog() {
    let blog_p = document.getElementById('blog_p').innerText;
    let blog = document.getElementById('entrada')
    blog.innerHTML = blog_p
}

escribirBlog();